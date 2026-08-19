import { useEffect, useRef } from "react"; 
import Nav from "../components/Nav";
import Footer from "../components/Footer";
import { useAgentChat } from "../../public/assets/js/agent.ts";
import "/public/assets/css/particles.css"; 



export default function Agent(){
  const {
    greetingText,
    inputValue,
    setInputValue, 
    messages,
    hasSubmitted,
    isGenerating, 
    handleSubmit,
    handleAttachFile
  } = useAgentChat();

  // Reference for the automatic scroll to the last message
  const messagesEndRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);



  return (
    <div className="min-h-screen text-white flex flex-col dark:bg-black">
      <Nav />

      <main className="flex-grow container mx-auto px-4 pt-20 pb-10 flex flex-col justify-between items-center text-center">

       {/* Dynamic light elements in the background */} 
        <div className="light x1"></div>
        <div className="light x2"></div>
        <div className="light x3"></div>
        <div className="light x4"></div>
        <div className="light x5"></div>
        <div className="light x6"></div>
        <div className="light x7"></div>
        <div className="light x8"></div>
        <div className="light x9"></div>
        
        {/* Depending on the user's query status (hasSubmitted), we modify the layout of the web */}
        {!hasSubmitted ? (
          <div className="flex-grow flex flex-col items-center justify-center w-full max-w-3xl">
            <h1 id="agentDynamicGreet" className="text-4xl text-gray-900 dark:text-white font-bold mb-8">AI Agent & RAG System</h1>
            <p className="text-gray-700 dark:text-gray-200 text-lg md:text-xl min-h-[3.5rem]">
              {greetingText}
              <span className="animate-pulse">|</span>
            </p>
          </div>
        ) : (
          <div className="flex-grow flex flex-col w-full max-w-4xl py-10 gap-6 text-left overflow-y-auto z-10 pr-2">
            {messages.map((message, index) => (
              <div 
                key={index}
                className={`flex w-full ${message.sender === "user" ? "justify-end" : "justify-start"}`}
              >
                {message.sender === "user" ? (
                  <div className=" bg-blue-600 text-white px-5 py-3 rounded-2xl rounded-br-none max-w-2xl shadow-md">
                    <p className="break-words">{message.text}</p>
                  </div>
                ) : (
                  <div className="bg-gray-200 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 text-gray-900 dark:text-gray-200 px-5 py-4 rounded-2xl rounded-bl-none w-full shadow-lg">
                    <p className="leading-relaxed">
                      {message.text}
                      {isGenerating && index === messages.length - 1 && (
                          <span className="animate-pulse ml-1">|</span>
                      )}
                    </p>
                  </div>
                )}
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>
        )}



        <form 
          onSubmit={handleSubmit}
          className="bg-gray-200 dark:bg-gray-900 backdrop-blur-md border border-gray-300 dark:border-gray-800 px-4 py-2.5 rounded-full w-full max-w-2xl shadow-2xl flex items-center gap-3 transition-all duration-300 z-20"
        >
          <button
            type="button"
            onClick={handleAttachFile}
            title="Attach files here"
            className="text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white hover:bg-gray-300 dark:hover:bg-gray-800 p-2 rounded-full transition-colors focus:outline-none"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 rotate-45" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
            </svg>
          </button>
          <input 
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            disabled={isGenerating}
            placeholder={isGenerating ? "The agent is generating the response..." : "Send a message..."}
            className="flex-grow bg-transparent text-gray-800 dark:text-gray-200 px-2 py-1.5 focus:outline-none placeholder-gray-400 dark:placeholder-gray-500 md:text-base disabled:opacity-50 disabled:cursor-not-allowed border-none"
          />
          <button
            type="submit"
            title="Send message to the agent"
            disabled={isGenerating || !inputValue.trim()}
            className="bg-blue-600 hover:bg-blue-800 dark:hover:bg-blue-700 text-white p-2.5 rounded-full font-medium transition-all disabled:opacity-40 disabled:cursor-not-allowed flex items-center justify-center"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 12h14M12 5l7 7-7 7" />
            </svg> 
          </button>
        </form>
      </main>

      <Footer />
    </div>
  );
}
