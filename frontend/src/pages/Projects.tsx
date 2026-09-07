import { Link } from "react-router-dom";
import Nav from "../components/Nav";
import Footer from "../components/Footer";
import "/public/assets/css/particles.css"; 
import "/public/assets/css/animation.css"; 



export default function Projects(){

  // We define the projects texts here so we can use them later 
  const projects = [
    {
      title: "RAG-Agent Tool",
      description: [
        "Providing a complete RAG (Retrieval Augmented Generation) System, where documents are chunked, embedded (with HuggingFace sentence-transformers), and stored in a vectorstore (ChromaDB). The Retrieval phase combines a dense and a sparse BM25 retriever, combined applying RRF (Reciprocal Rank Fusion) for better performance",
        "Combined with an AI agent built with LangGraph, the system decides whether to retrieve users documents uploaded previously or search recent information from internet (via Tavily). These web results are correctly indexed back into the vectorstore and the agent loops between reasoning and tool use until it has enough context to answer (ReAct)",
        "Finally, this agent that implements the RAG system and web search tools is handled though FastAPI backend in this portfolio. As in a production system, per-user cookie-based sessions, email verification, and SQLite requests are managed to access the agent. This is available in AI Demo, handling prompts and file uploads, full chat history persistance, and a alert system sent to the administrator on critical failures, Make sure to check it out!"
      ],
      images: ["./assets/images/ai_chat_demo_dark.png", "./assets/images/ai_chat_code.png"],
      tech: ["Python", "LangChain", "LangGraph", "RAG", "Agentic AI", "FastAPI", "ChromaDB", "MySQL", "TypeScript", "React"],
      github: "https://github.com/rnoguer22/Portfolio",
      demo: "/agent"
    },
    {
      title: "Real-Time Intrusion Detection System IDS",
      description: [
        "This is one of my undergraduate thesis, where a real-time IDS is developed for web services, combining supervised and unsupervised learning, where an undercomplete Autoencoder, trained exclusively on benign traffic, flags anomalous network flows based on its reconstruction error (MSE), while a Random Forest classifier subsequently categorizes the detected threat (DoS, brute force, SQL injection, among others)",
        "The model was trained on the CICIDS2017 reference dataset, with careful feature selection guided by correlation analysis and other measurements to remove hardware and environment-dependent variables, improving the real time detection of anomalous traffic. It is based on a LAMP architecture which allows perform real penetration testing evaluations using SQLMap or Hydra, with network flows extracted in real time via NFStream. If you want to learn more, check the project on Github!"
      ],
      images: ["./assets/images/class_distribution_malign.png", "./assets/images/matriz_correlacion_dark.png", "./assets/images/sqlmap_attack.png"],
      tech: ["Python", "Machine Learning", "Deep Learning", "Cybersecurity", "Scikit-learn", "Pandas", "Numpy", "NFStream", "Linux"],
      github: "https://github.com/rnoguer22/AnomaliasTFG",
    },
  ];

  return (
    <div className="min-h-screen h-full text-gray-900 dark:text-white flex flex-col bg-white dark:bg-black">
      <div className="relative z-[110]">
          <Nav />
      </div>

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

        <section className="pt-20 pb-8 text-center relative z-10">
          <div className="max-w-screen-md mx-auto px-4">
            <h1 className="mb-4 text-4xl font-extrabold tracking-tight leading-none md:text-5xl xl:text-6xl text-gray-900 dark:text-white">
              My <span className="text-blue-500">Projects</span>
            </h1>
            <p className="text-gray-500 text-2xl dark:text-gray-400">
              An overview of the main work I have built over the last months, combining mathematics, software engineering and AI
            </p>
          </div>
        </section>

        {/* Projects list */}
        {projects.map((project, index) => (
          <section
            key={project.title}
            id={`project-${index + 1}`}
            className={`relative z-10 ${
              index !== projects.length - 1 ? "border-b-4 border-solid border-blue-700" : ""
            }`}
          >
            <div
              className={`gap-16 items-center py-16 px-4 mx-auto max-w-screen-xl lg:grid lg:grid-cols-2 lg:px-6 ${
                index % 2 === 1 ? "lg:[&>*:first-child]:order-2" : ""
              }`}
            >
              {/* Text */}
              <div className="text-left">
                <span className="inline-block mb-3 text-sm font-bold uppercase tracking-widest text-blue-500">
                  Project 0{index + 1}
                </span>
                <h2 className="mb-4 text-3xl md:text-4xl tracking-tight font-extrabold text-gray-900 dark:text-white">
                  {project.title}
                </h2>

                {project.description.map((paragraph, pIndex) => (
                  <p
                    key={pIndex}
                    className="mb-4 font-light text-gray-500 dark:text-gray-400 text-lg lg:text-xl"
                  >
                    {paragraph}
                  </p>
                ))}

                {/* Tech skill*/}
                <div className="flex flex-wrap gap-2 mt-6 mb-8">
                  {project.tech.map((tech) => (
                    <span
                      key={tech}
                      className="px-3 py-1 text-sm font-bold text-blue-700 dark:text-blue-400 border-2 border-blue-300 dark:border-blue-700 rounded-full"
                    >
                      {tech}
                    </span>
                  ))}
                </div>

                {/* Buttons */}
                <div className="flex flex-wrap gap-3">
                  <a
                    href={project.github}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center justify-center px-5 py-3 text-base font-medium text-center text-gray-900 dark:text-white bg-primary-700 hover:bg-primary-800 focus:ring-4 focus:ring-primary-300 dark:focus:ring-primary-900 transition-all duration-300"
                  >
                    View on GitHub
                    <svg
                      className="w-5 h-5 ml-2 -mr-1"
                      fill="currentColor"
                      viewBox="0 0 24 24"
                      xmlns="http://www.w3.org/2000/svg"
                    >
                      <path
                        fillRule="evenodd"
                        d="M12.006 2a9.847 9.847 0 0 0-6.484 2.44 10.32 10.32 0 0 0-3.393 6.17 10.48 10.48 0 0 0 1.317 6.955 10.045 10.045 0 0 0 5.4 4.418c.504.095.683-.223.683-.494 0-.245-.01-1.052-.014-1.908-2.78.62-3.366-1.21-3.366-1.21a2.711 2.711 0 0 0-1.11-1.5c-.907-.637.07-.621.07-.621.317.044.62.163.885.346.266.183.487.426.647.71.135.253.318.476.538.655a2.079 2.079 0 0 0 2.37.196c.045-.52.27-1.006.635-1.37-2.219-.259-4.554-1.138-4.554-5.07a4.022 4.022 0 0 1 1.031-2.75 3.77 3.77 0 0 1 .096-2.713s.839-.275 2.749 1.05a9.26 9.26 0 0 1 5.004 0c1.906-1.325 2.74-1.05 2.74-1.05.37.858.406 1.828.101 2.713a4.017 4.017 0 0 1 1.029 2.75c0 3.939-2.339 4.805-4.564 5.058a2.471 2.471 0 0 1 .679 1.897c0 1.372-.012 2.477-.012 2.814 0 .272.18.592.687.492a10.05 10.05 0 0 0 5.388-4.421 10.473 10.473 0 0 0 1.313-6.948 10.32 10.32 0 0 0-3.39-6.165A9.847 9.847 0 0 0 12.007 2Z"
                        clipRule="evenodd"
                      />
                    </svg>
                  </a>
                  {project.demo && (
                    <Link to={project.demo}
                      className="inline-flex items-center justify-center px-5 py-3 text-base font-medium text-center text-gray-900 border-4 border-blue-300 hover:bg-blue-100 focus:ring-4 focus:ring-gray-100 dark:text-white dark:border-blue-700 dark:hover:bg-blue-700 dark:focus:ring-gray-800 transition-all duration-300"
                    >
                      Live Demo
                    </Link>
                  )}
                </div>
              </div>

              {/* Image */}
              <div className="flex flex-col gap-12 mt-8 lg:mt-0">
                {project.images.length >= 3 ? (
                  <>
                    {/* First row, containing a whole image */}
                    <div className="w-full">
                      <img
                        className={"w-full rounded-xl shadow-2xl transition-all duration-300 hover:saturate-150 hover:brightness-90 hover:scale-[1.02] hover:rotate-0 hover:z-10 relative"}
                        src={project.images[0]}
                        alt={`${project.title} - 1`}
                      />
                    </div>
                    {/* Second row, with the rest of the images */}
                    <div className={"grid grid-cols-1 md:grid-cols-2 gap-12"}>
                      {project.images.slice(1).map((img, index) => (
                        <img
                          key={index + 1}
                          className={`w-full rounded-xl shadow-2xl transition-all duration-300 hover:saturate-150 hover:brightness-90 hover:scale-[1.02] hover:rotate-0 hover:z-10 relative ${
                            index % 2 !== 0 ? "lg:rotate-1 lg:ml-0" : "lg:-rotate-1 lg:ml-6"
                          }`}
                          src={img}
                          alt={`${project.title} - ${index + 2}`}
                        />
                      ))}
                    </div>
                  </>
                ) : (
                  project.images.map((img, index) => (
                    <img
                      key={index}
                      className={`w-full rounded-xl shadow-2xl transition-all duration-300 hover:saturate-150 hover:brightness-90 hover:scale-[1.02] hover:rotate-0 hover:z-10 relative ${
                        index % 2 === 0 ? "lg:rotate-1 lg:ml-0" : "lg:-rotate-1 lg:ml-6"
                      }`}
                      src={img}
                      alt={`${project.title} - ${index + 1}`}
                    />
                  ))
                )}
              </div>
            </div>
          </section>
        ))}

        <section className="py-10 text-center relative z-10">
          <div className="max-w-screen-md mx-auto px-4">
            <h2 className="mb-4 text-3xl md:text-4xl tracking-tight font-extrabold text-gray-900 dark:text-white">
              Want to see more?
            </h2>
            <p className="mb-8 font-light text-gray-500 dark:text-gray-400 text-xl">
              Check out the rest of my work and experiments directly on GitHub.
            </p>
            <a
              href="https://github.com/rnoguer22"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center justify-center px-5 py-4 text-base font-medium text-center text-gray-900 border-4 border-blue-300 hover:bg-blue-100 focus:ring-4 focus:ring-gray-100 dark:text-white dark:border-blue-700 dark:hover:bg-blue-700 dark:focus:ring-gray-800 transition-all duration-300"
            >
              Visit My GitHub
            </a>
          </div>
        </section>
        
      </main>
      <Footer />
    </div>
  );
}
