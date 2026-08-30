// public/assets/js/agent.js
import { useState, useEffect } from "react";



export function useAgentChat() {

  // Define useState variuables
  const [greetingText, setGreetingText] = useState("");
  const [inputPrompt, setInputPrompt] = useState("");
  const [selectedFile, setSelectedFile] = useState<FIle | null>(null);

  // We read the chat history as it follows, so that when we return to AI-demo we see the messages we had sent before
  const [messages, setMessages] = useState(() => {
    const saved = localStorage.getItem("chat_history");
    return saved ? JSON.parse(saved) : [];
  });
  const [hasSubmitted, setHasSubmitted] = useState(() => {
    const saved = localStorage.getItem("chat_history");
    return saved ? JSON.parse(saved).length > 0 : false;
  });

  const [isGenerating, setIsGenerating] = useState(false);

  const initText = "Good morning! What's on your mind today?";
  const [response, setResponse] = useState("");



  // Display the initial greet variable with a cool effect
  useEffect(() => {
    let index = 0;
    const interval = setInterval(() => {
      if (index <= initText.length) {
        setGreetingText(initText.substring(0, index));
        index++;
      } else {
        clearInterval(interval);
      }
    }, 50);

    return () => clearInterval(interval)
  }, []);

  // Save the chat_history so that we return to AI-demo we see the old messages from before
  useEffect(() => {
    localStorage.setItem("chat_history", JSON.stringify(messages));
  }, [messages]);



  // Next we manage the response generated from the llm in the back, updating some useState variables to change the interface as we go generating
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputPrompt.trim() || isGenerating){
      return;
    }

    const userText = inputPrompt;
    setInputPrompt("");
    setHasSubmitted(true);
    setIsGenerating(true);

    // We add the user query to the history of messages 
    setMessages((prev) => [...prev, { sender: "user", text: userText, fileName: selectedFile ? selectedFile.name : null }]);

    // Connection with backend FastAPI
    try {
      const formData = new FormData();
      formData.append("prompt", userText);
      // If theres a selected file, we add it to the form data 
      if (selectedFile){
        formData.append("file", selectedFile);
        setSelectedFile(null);
      }

      // We use AbortController to handle timeouts from the server, avoiding the chat to get frozen
      const abortController = new AbortController();
      const timeoutId = setTimeout(() => {
        abortController.abort();
      }, 30000);

      const res = await fetch("http://localhost:8000/agent", {
        method: "POST",
        body: formData,
        signal: abortController.signal, // Assign the abortController instance to start
        credentials: "include" // To get the cookies
      });

      // Wait for the backend and llm to generate the response
      console.log("Sending data...");
      const data = await res.json();
      console.log("Data received: ", data);

      let responseAgent = "";
      if (data.error) {
        responseAgent = data.error;
      } else if (data.message) {
        responseAgent = data.message;
      } else {
        responseAgent = "Error, please try again later."
      }

      setMessages((prev) => [
        ...prev, 
        {sender: "agent", text: responseAgent}
      ]);
      setIsGenerating(false);

    } catch (error) {
      let errorMessage = "";
      // If AbortController exceeds the limit time, we return a time out error
      if (error.name === "AbortError") {
        errorMessage = "Error: Connection timed out. Please try again later...";
      } else {
        // Generic error 
        errorMessage = "Error: Connection to the server refused. Please try again later...";
      }
      console.error(errorMessage, error);
      setMessages((prev) => [...prev, { sender: "agent", text: errorMessage}]);
      setIsGenerating(false)
    }
  };

  

  const handleAttachFile = () => {
    const fileInput = document.createElement("input");
    fileInput.type = "file";

    fileInput.onchange = (e: Event) => {
      const target = e.target as HTMLInputElement;
      if (target.files && target.files.length > 0) {
        const file = target.files[0];
        setSelectedFile(file);
        console.log("File loaded successfully: ", file.name, " Size: ", file.size, " bytes");
      }
    };
    fileInput.click();
  }

  const handleRemoveFile = () => {
    setSelectedFile(null);
  }



  return {
    greetingText,
    inputPrompt,
    setInputPrompt, 
    selectedFile,
    messages,
    hasSubmitted,
    isGenerating,
    handleSubmit,
    handleAttachFile,
    handleRemoveFile
  };

}
