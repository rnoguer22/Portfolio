// public/assets/js/agent.js
import { useState, useEffect } from "react";



export function useAgentChat() {

  // Define useState variuables
  const [greetingText, setGreetingText] = useState("");
  const [inputValue, setInputValue] = useState("");
  const [messages, setMessages] = useState([]);
  const [hasSubmitted, setHasSubmitted] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);

  const initText = "Good morning! What's on your mind today?";
  const response = "¡Hola! He recibido tu mensaje de prueba desde la interfaz separada. Pronto lo conectaremos con FastAPI. \n\nLorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since 1966, when designers at Letraset and James Mosley, the librarian at St Bride Printing Library in London, took a 1914 Cicero translation and scrambled it to make dummy text for Letraset's Body Type sheets. It has survived not only many decades, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised thanks to these sheets and more recently with desktop publishing software like Aldus PageMaker and Microsoft Word including versions of Lorem Ipsum.";

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



  // Next we handle the rest od the useState props 
  // This way we know when the user's query's been submitted, when the llm is generating text, etc.
  // Enabling us to modify the interface 
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || isGenerating){
      return;
    }

    const userText = inputValue;
    setInputValue("");
    setHasSubmitted(true);
    setIsGenerating(true);

    // We add the user query to the history of messages 
    setMessages((prev) => [...prev, { sender: "user", text: userText }]);
    // We also add the agent's response (not implemmented. For the moment is just a lorem ipsum)
    setMessages((prev) => [...prev, { sender: "agent", text: "" }]);

    let index = 0;
    const interval = setInterval(() => {
      if (index <= response.length) {
        const currentSlice = response.substring(0, index);

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
    }, 2.5);
  };

  

  const handleAttachFile = () => {
    const fileInput = document.createElement("input");
    fileInput.type = "file";
    fileInput.click();
  }

  return {
    greetingText,
    inputValue,
    setInputValue, 
    messages,
    hasSubmitted,
    isGenerating, 
    handleSubmit,
    handleAttachFile
  };

}
