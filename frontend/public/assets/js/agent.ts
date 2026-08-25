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
    setMessages((prev) => [...prev, { sender: "agent", text: "" }]);

    // Connection with backend FastAPI
    try {
      const formData = new FormData();
      formData.append("prompt", userText);
      // If theres a selected file, we add it to the form data 
      if (selectedFile){
        formData.append("file", selectedFile);
        setSelectedFile(null);
      }

      const res = await fetch("http://localhost:8000/agent", {
        method: "POST",
        body: formData
      });

      // Wait for the backend and llm to generate the response
      console.log("Sending data...");
      const data = await res.json();
      console.log("Data received: ", data);
      const llmResponse = data.message;

      let index = 0;
      const interval = setInterval(() => {
        if (index <= llmResponse.length) {
          const currentSlice = llmResponse.substring(0, index);
          // Update the last response message as we go generating, so that we can scroll while the response is being created
          setMessages((prev) => {
            const newMessages = [...prev];
            newMessages[newMessages.length - 1] = { sender: "agent", text: currentSlice };
            return newMessages;
          });

          index++;
        } else {
          clearInterval(interval);
          setIsGenerating(false);
        }
      }, 10);

    } catch (error) {
      errorMessage = "Error connecting with backend";
      console.error(errorMessage, error);
      setMessages((prev) => [...prev.slice(0, -1), { sender: "agent", text: errorMessage}])
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
