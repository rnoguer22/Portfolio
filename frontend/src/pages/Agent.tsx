import { useEffect, useRef } from "react"; 
import ReactMarkdown from "react-markdown";
import Nav from "../components/Nav";
import Footer from "../components/Footer";
import { useAgentChat } from "../../public/assets/js/agent.ts";
import { emailAuth } from "../../public/assets/js/emailAuth.ts";
import "/public/assets/css/particles.css"; 
import "/public/assets/css/animation.css"; 



export default function Agent(){
  const {
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
  } = useAgentChat();

  const {
    isVerified,
    isAuthModalOpen,
    authStep,
    setAuthStep,
    authEmail,
    setAuthEmail,
    authCode,
    setAuthCode,
    authLoading,
    authMessage,
    handleRequestOtp,
    handleVerifyOtp
  } = emailAuth();

  // Reference for the automatic scroll to the last message
  const messagesEndRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);



  return (
    <div className="min-h-screen text-white flex flex-col dark:bg-black">
      <div className="relative z-[110]">
          <Nav />
      </div>

      {/* Modal de Bloqueo Automático por Correo */}
      {isAuthModalOpen && (
        <div className="font-mono fixed inset-0 z-[100] flex items-center justify-center bg-black/80 backdrop-blur-sm p-4 animate-[fadeIn_0.3s_ease-out]">
          <div className="bg-white dark:bg-gray-900 border border-gray-300 dark:border-gray-800 rounded-2xl p-6 w-full max-w-md shadow-2xl text-left relative">
            <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">
              {authStep === "email" ? "Restricted access" : "Verify code"}
            </h3>
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-6">
              {authStep === "email" 
                ? "Please introduce your email and we will send you a verification code to start using the AI agent!"
                : `Introduce the code sent to ${authEmail}.`}
            </p>

            {authStep === "email" ? (
              <form onSubmit={handleRequestOtp} className="space-y-4">
                <input 
                  type="email"
                  value={authEmail}
                  onChange={(e) => setAuthEmail(e.target.value)}
                  placeholder="your.email@example.com"
                  required
                  className="w-full bg-gray-100 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-xl px-4 py-2.5 text-gray-900 dark:text-white focus:outline-none focus:border-blue-500 font-mono text-sm"
                />
                <button
                  type="submit"
                  disabled={authLoading}
                  className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2.5 rounded-xl transition-all disabled:opacity-50"
                >
                  {authLoading ? "Sending..." : "Send code"}
                </button>
              </form>
            ) : (
              <form onSubmit={handleVerifyOtp} className="space-y-4">
                <input 
                  type="text"
                  value={authCode}
                  onChange={(e) => setAuthCode(e.target.value)}
                  placeholder="123456"
                  required
                  className="w-full bg-gray-100 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-xl px-4 py-2.5 text-center tracking-widest text-lg text-gray-900 dark:text-white focus:outline-none focus:border-blue-500 font-mono"
                />
                <button
                  type="submit"
                  disabled={authLoading}
                  className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2.5 rounded-xl transition-all disabled:opacity-50"
                >
                  {authLoading ? "Verifying..." : "Verify and access the tool"}
                </button>
                <button
                  type="button"
                  onClick={() => setAuthStep("email")}
                  className="w-full text-xs text-gray-500 hover:text-gray-700 dark:hover:text-gray-300 text-center mt-2"
                >
                  Misstyped the email? Change it
                </button>
              </form>
            )}

            {authMessage && (
              <p className={`mt-4 text-xs text-center ${authMessage.includes("successfull") || authMessage.includes("successfully") ? "text-green-500" : "text-red-500"}`}>
                {authMessage}
              </p>
            )}
          </div>
        </div>
      )}

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
          <div className="font-mono flex-grow flex flex-col w-full max-w-4xl py-10 gap-6 text-left overflow-y-auto z-10 pr-2">
            {messages.map((message, index) => (
              <div 
                key={index}
                className={`flex w-full ${message.sender === "user" ? "justify-end" : "justify-start"}`}
              >
                {message.sender === "user" ? (
                  <div className="bg-blue-600 text-white px-5 py-3 rounded-2xl rounded-br-none max-w-2xl shadow-md">
                    {message.fileName && (
                      <div className="mb-2 bg-blue-700/80 border border-blue-500 text-white text-xs px-3 py-1.5 rounded-xl shadow-sm flex items-center gap-2 w-fit">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 text-blue-200 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                        <span className="truncate max-w-[200px] font-medium">{message.fileName}</span>
                      </div>
                    )}
                    <p className="break-words">{message.text}</p>
                  </div>
                ) : (
                  <div className="bg-gray-200 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 text-gray-900 dark:text-gray-200 px-5 py-4 rounded-2xl rounded-bl-none w-full shadow-lg animate-[fadeIn_1.5s_ease-out_forwards]">
                    <div className="leading-relaxed prose dark:prose-invert max-w-none inline">
                      <ReactMarkdown
                        components={{
                          pre: ({node, ...props}) => (
                            <div className="overflow-x-auto my-3 p-3 bg-gray-100 text-gray-900 dark:bg-gray-900 dark:text-gray-100 rounder-xl border border-gray-300 dark:border-gray-700 shadow-inner">
                              <pre {...props} /> 
                            </div>
                          ), 
                          code: ({node, inline, ...props}: any) =>
                            inline ? (
                              <code className="bg-gray-300 dark:bg-gray-700 px-1.5 py-0.5 rounded text-xs font-mono" {...props} />
                            ) : (
                              <code className="font-mono text-xs md:text-sm block" {...props} />
                            ),
                          p: ({node, ...props}) => <p className="mb-2 last:mb-0" {...props} /> 
                        }}
                      >
                        {message.text}
                      </ReactMarkdown>
                      {isGenerating && index === messages.length - 1 && (
                          <span className="animate-pulse inline-block ml-0.5 font-bold">|</span>
                      )}
                    </div>
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
          {/* Selected File display */}
          {selectedFile && (
            <div className="absolute bottom-full left-4 mb-2 bg-gray-200 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 text-gray-800 dark:text-gray-200 text-xs px-3 py-1.5 rounded-xl shadow-lg flex items-center gap-2 z-30 animate-fade-in">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 text-blue-500 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <span className="truncate max-w-[200px] font-medium">{selectedFile.name}</span>
              <button 
                type="button"
                onClick={handleRemoveFile}
                className="text-gray-400 hover:text-red-500 transition-colors ml-1 focus:outline-none"
                title="Remove file"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          )}
          <button
            type="button"
            onClick={handleAttachFile}
            title="Attach files here"
            disabled={isGenerating}
            className="text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white hover:bg-gray-300 dark:hover:bg-gray-800 p-2 rounded-full transition-colors focus:outline-none disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 rotate-45" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
            </svg>
          </button>
          <div className="flex-grow flex items-center min-w-0 overflow-hidden px-2 py-1.5">
            {isGenerating ? (
              <span className="typing-placeholder font-mono text-gray-400 dark:text-gray-500 text-left md:text-base">
                The agent is generating the response...
              </span>
            ) : (
              <input 
                type="text"
                value={inputPrompt}
                onChange={(e) => setInputPrompt(e.target.value)}
                placeholder="Send a message..."
                disabled={!isVerified}
                className="font-mono w-full bg-transparent text-gray-800 dark:text-gray-200 focus:outline-none placeholder-gray-400 dark:placeholder-gray-500 md:text-base border-none text-left"
              />
            )}
          </div>
          <button
            type="submit"
            title="Send message to the agent"
            disabled={isGenerating || !inputPrompt.trim() &&!selectedFile}
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
