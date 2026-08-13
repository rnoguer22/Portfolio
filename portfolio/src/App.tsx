// src/App.tsx
import React from "react";
import Nav from "./components/Nav";
import Footer from "./components/Footer";
import "/public/assets/css/particles.css"; 



const App: React.FC = () => {
  return (
    <>
      <Nav />
      <main id="home" className="w-full">
       {/* Floating light elements contained within the hero section */} 

        <div className="light x1"></div>
        <div className="light x2"></div>
        <div className="light x3"></div>
        <div className="light x4"></div>
        <div className="light x5"></div>
        <div className="light x6"></div>
        <div className="light x7"></div>
        <div className="light x8"></div>
        <div className="light x9"></div>
      
      {/* #### HERO SECTION #### */}
      
      <section className="pt-20 md:pt-0 bg-white dark:bg-black">

      <div className="grid max-w-screen-xl px-4 py-8 mx-auto lg:gap-8 xl:gap-0 lg:py-32 lg:grid-cols-12 relative z-10">
        <div className="mr-auto place-self-center lg:col-span-7">
        <h1
            id="dynamicHeadline"
            className="max-w-2xl mb-4 text-4xl font-extrabold tracking-tight leading-none md:text-5xl xl:text-6xl dark:text-white"
          >
            Driving The Future{" "}
            <span id="dynamicWords" className="text-blue-500 font-bold">
              Building The Next Generation of AI
            </span>
          </h1>

          <p className="max-w-2xl mb-6 font-bold text-gray-500 lg:mb-8 text-3xl dark:text-gray-400">
            From Machine Learning and Deep Learning models to LLM-powered RAG and agentic AI systems, I build intelligent solutions that turn data into real-world impact.
          </p>
          <a
            href="#about"
            className="inline-flex items-center justify-center px-5 py-3 mr-3 text-base font-medium text:3xl text-center text-white  bg-primary-700 hover:bg-primary-800 focus:ring-4 focus:ring-primary-300 dark:focus:ring-primary-900"
          >
            More About Me
            <svg
              className="w-5 h-5 ml-2 -mr-1"
              fill="currentColor"
              viewBox="0 0 20 20"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                fillRule="evenodd"
                d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z"
                clipRule="evenodd"
              />
            </svg>
          </a>
          <a
            href="#contact"
            className="inline-flex items-center justify-center px-5 py-4 text-base font-medium text:3xl text-center text-gray-900 border-4 border-blue-300  hover:bg-blue-100 focus:ring-4 focus:ring-gray-100 dark:text-white dark:border-blue-700 dark:hover:bg-blue-700 dark:focus:ring-gray-800"
          >
            Contact Me!
          </a>
        </div>
        <div 
          id="hacker-logo" 
          className="lg:mt-0 lg:col-span-5 lg:flex relative z-10"
          style={{ opacity: 0 }}  // This ensures it's initially invisible but still rendered
        >
          <img
            src="./assets/images/portfolio.png"
            alt="Ruben"
          />
        </div>
      </div>
    </section>

    {/* #### ACCOLADES SECTION #### */}
        <section className="bg-white dark:bg-black ">
          <div className="max-w-screen-xl px-4 py-8 mx-auto text-center lg:py-28 lg:px-6 border-4 border-solid border-blue-700 bg-white dark:bg-black relative z-20">
          <dl className="grid max-w-screen-md gap-8 mx-auto text-gray-900 sm:grid-cols-3 dark:text-white">
              <div className="flex flex-col items-center justify-center">
                  <dt className="mb-2 text-5xl md:text-7xl font-extrabold">
                      <span data-counter-target="5 years">0</span>+
                  </dt>
                  <dd className="font-light text-2xl text-gray-500 dark:text-gray-400">AI Years of Experience</dd>
              </div>
              <div className="flex flex-col items-center justify-center">
                  <dt className="mb-2 text-5xl md:text-7xl font-extrabold">
                      <span data-counter-target="100">0</span>+
                  </dt>
                  <dd className="font-light text-2xl text-gray-500 dark:text-gray-400">Projects in Github</dd>
              </div>
              <div className="flex flex-col items-center justify-center">
                  <dt className="mb-2 text-5xl md:text-7xl font-extrabold">
                      <span data-counter-target="10000">0</span>
                  </dt>
                  <dd className="font-light text-2xl text-gray-500 dark:text-gray-400">Cups of Dark Roast Coffee</dd>
              </div>
          </dl>
                    </div>
                    
        </section>

        {/* #### SERVICES SECTION #### */}
          <section id="services" className="pt-8 pb-12 bg-white dark:bg-black flex justify-center items-center">
          <div className="py-8 px-4 mx-auto max-w-screen-xl sm:py-16 lg:px-6 text-center">

              <div className="max-w-screen-md mb-8 lg:mb-12 mx-auto">
                <h2 className="mb-4 text-4xl md:text-5xl tracking-tight font-extrabold text-gray-900 dark:text-white">
                  Where Mathematics and Technology Meet
                </h2>
                <p className="text-gray-500 text-2xl dark:text-gray-400">
                  Combining mathematical thinking with software engineering to explore, build and solve complex problems through data and intelligent systems.
                </p>
              </div>

              <div className="space-y-8 md:grid md:grid-cols-2 lg:grid-cols-3 md:gap-12 md:space-y-0">
              <div className="transform transition-all duration-300 hover:scale-105 group">
                  <div className="flex justify-center mx-auto items-center mb-4 w-10 h-10 rounded-full bg-primary-100 lg:h-12 lg:w-12 dark:bg-primary-900">
                    <svg
                      className="w-[48px] h-[48px] text-gray-800 dark:text-white transition-colors duration-300 group-hover:text-blue-500 group-hover:scale-125"
                      aria-hidden="true"
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 24 24"
                      fill="none"
                    >
                      <rect x="4" y="6" width="16" height="13" rx="3" stroke="currentColor" strokeWidth="1.5"/>
                      <path d="M12 3V6" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                      <circle cx="9" cy="12" r="1" fill="currentColor" />
                      <circle cx="15" cy="12" r="1" fill="currentColor" />
                      <path d="M9 16h6" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                      <path d="M2 11v3M22 11v3" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                    </svg>
                  </div>
                  <h3 className="mb-2 text-3xl font-bold dark:text-white">LLMs & AI Agents</h3>
                  <p className="text-gray-500 text-xl dark:text-gray-400">
                    Developing LLM-powered applications and autonomous agents using Python, LangChain and LangGraph, with tool calling and external data sources.
                  </p>
                </div>

                <div className="transform transition-all duration-300 hover:scale-105 group">
                  <div className="flex justify-center mx-auto items-center mb-4 w-10 h-10 rounded-full bg-primary-100 lg:h-12 lg:w-12 dark:bg-primary-900">
                    <svg
                      className="w-[48px] h-[48px] text-gray-800 dark:text-white transition-colors duration-300 group-hover:text-blue-500 group-hover:scale-125"
                      aria-hidden="true"
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 24 24"
                      fill="none"
                    >
                      <ellipse cx="10" cy="5" rx="6" ry="2.5" stroke="currentColor" strokeWidth="1.5"/>
                      <path d="M4 5v6c0 1.38 2.69 2.5 6 2.5s6-1.12 6-2.5V5" stroke="currentColor" strokeWidth="1.5"/>
                      <path d="M4 11v6c0 1.38 2.69 2.5 6 2.5 1.17 0 2.25-.15 3.16-.42" stroke="currentColor" strokeWidth="1.5"/>
                      <circle cx="17.5" cy="17.5" r="3" stroke="currentColor" strokeWidth="1.5"/>
                      <path d="m20 20 2 2" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                    </svg>
                  </div>
                  <h3 className="mb-2 text-3xl font-bold dark:text-white">RAG Systems</h3>
                  <p className="text-gray-500 text-xl dark:text-gray-400">
                    Designing Retrieval-Augmented Generation systems that combine LLMs with document retrieval, embeddings and external knowledge to build grounded AI applications.
                  </p>
                </div>
                <div className="transform transition-all duration-300 hover:scale-105 group">
                  <div className="flex justify-center mx-auto items-center mb-4 w-10 h-10 rounded-full bg-primary-100 lg:h-12 lg:w-12 dark:bg-primary-900">
                    <svg
                      className="w-[48px] h-[48px] text-gray-800 dark:text-white transition-colors duration-300 group-hover:text-blue-500 group-hover:scale-125"
                      aria-hidden="true"
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 24 24"
                      fill="none"
                    >
                      <circle cx="5" cy="7" r="2" stroke="currentColor" strokeWidth="1.5"/>
                      <circle cx="5" cy="17" r="2" stroke="currentColor" strokeWidth="1.5"/>
                      <circle cx="12" cy="12" r="2" stroke="currentColor" strokeWidth="1.5"/>
                      <circle cx="19" cy="7" r="2" stroke="currentColor" strokeWidth="1.5"/>
                      <circle cx="19" cy="17" r="2" stroke="currentColor" strokeWidth="1.5"/>
                      <path d="M7 7.5 10 11M7 16.5 10 13M14 11l3-3.5M14 13l3 3.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                    </svg>
                  </div>
                  <h3 className="mb-2 text-3xl font-bold dark:text-white">Machine Learning</h3>
                  <p className="text-gray-500 text-xl dark:text-gray-400">
                    Developing Machine Learning models for classification, prediction and anomaly detection, with a focus on extracting meaningful patterns from real-world datasets.
                  </p>
                </div>
                <div className="transform transition-all duration-300 hover:scale-105 group">
                  <div className="flex justify-center mx-auto items-center mb-4 w-10 h-10 rounded-full bg-primary-100 lg:h-12 lg:w-12 dark:bg-primary-900">
                    <svg
                      className="w-[48px] h-[48px] text-gray-800 dark:text-white transition-colors duration-300 group-hover:text-blue-500 group-hover:scale-125"
                      aria-hidden="true"
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 24 24"
                      fill="none"
                    >
                      <path d="M2.5 12s3.5-6 9.5-6 9.5 6 9.5 6-3.5 6-9.5 6-9.5-6-9.5-6Z" stroke="currentColor" strokeWidth="1.5" strokeLinejoin="round"/>
                      <circle cx="12" cy="12" r="3" stroke="currentColor" strokeWidth="1.5"/>
                      <circle cx="12" cy="12" r="1" fill="currentColor"/>
                    </svg>
                  </div>
                  <h3 className="mb-2 text-3xl font-bold dark:text-white">Deep Learning & Computer Vision</h3>
                  <p className="text-gray-500 text-xl dark:text-gray-400">
                    Building Deep Learning models for image classification and computer vision using TensorFlow/Keras and convolutional neural networks.
                  </p>
                </div>
                <div className="transform transition-all duration-300 hover:scale-105 group">
                  <div className="flex justify-center mx-auto items-center mb-4 w-10 h-10 rounded-full bg-primary-100 lg:h-12 lg:w-12 dark:bg-primary-900">
                    <svg
                      className="w-[48px] h-[48px] text-gray-800 dark:text-white transition-colors duration-300 group-hover:text-blue-500 group-hover:scale-125"
                      aria-hidden="true"
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 24 24"
                      fill="none"
                    >
                      <path d="M4 19V5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                      <path d="M4 19h16" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                      <path d="m7 15 4-4 3 2 5-6" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                      <circle cx="7" cy="15" r="1" fill="currentColor"/>
                      <circle cx="11" cy="11" r="1" fill="currentColor"/>
                      <circle cx="14" cy="13" r="1" fill="currentColor"/>
                      <circle cx="19" cy="7" r="1" fill="currentColor"/>
                    </svg>
                  </div>
                  <h3 className="mb-2 text-3xl font-bold dark:text-white">Data & Computational Engineering</h3>
                  <p className="text-gray-500 text-xl dark:text-gray-400">
                    Working with Python and mathematical methods to process, analyse and model complex datasets, combining data science with software engineering.
                  </p>
                </div>
                <div className="transform transition-all duration-300 hover:scale-105 group">
                  <div className="flex justify-center mx-auto items-center mb-4 w-10 h-10 rounded-full bg-primary-100 lg:h-12 lg:w-12 dark:bg-primary-900">
                    <svg
                      className="w-[48px] h-[48px] text-gray-800 dark:text-white transition-colors duration-300 group-hover:text-blue-500 group-hover:scale-125"
                      aria-hidden="true"
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 24 24"
                      fill="none"
                    >
                      <rect x="3" y="4" width="18" height="16" rx="2" stroke="currentColor" strokeWidth="1.5"/>
                      <path d="m7 9 3 3-3 3" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                      <path d="M12 15h4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                    </svg>
                  </div>
                  <h3 className="mb-2 text-3xl font-bold dark:text-white">Linux</h3>
                  <p className="text-gray-500 text-xl dark:text-gray-400">
                    Linux is part of my daily development environment, from system configuration and scripting to development workflows and infrastructure.
                  </p>
                </div>
              </div>
            </div>
          </section>
          
          {/* #### LOGOS SECTION #### */}
          <section className="bg-gray-100 dark:bg-black lg:py-18 lg:px-6 border-t-4 border-b-4 border-solid border-blue-700 relative z-20">
            <div className="py-8 lg:py-16 mx-auto max-w-screen-xl px-4">
              <h2 className="mb-8 lg:mb-16 text-3xl font-extrabold tracking-tight leading-tight text-center text-gray-900 dark:text-white md:text-4xl">
                Experience
              </h2>
              <div className="grid grid-cols-2 gap-8 mx-24 text-gray-500 sm:gap-12 md:grid-cols-2 lg:grid-cols-2 dark:text-gray-400">
                <a href="#" className="flex justify-center items-center group">
                  <img
                    src="/assets/images/ey_logo.png"
                    alt="EY"
                    className="h-12 w-auto object-contain opacity-70 transition-all duration-300 group-hover:opacity-100 group-hover:scale-110"
                  />
                </a>
                <a href="#" className="flex justify-center items-center group">
                  <img
                    src="/assets/images/accenture_logo.png"
                    alt="Accenture"
                    className="h-12 w-auto object-contain opacity-70 transition-all duration-300 group-hover:opacity-100 group-hover:scale-110"
                  />
                </a>
              </div>
            </div>
          </section>

          {/* #### SERVICES SECTION #### */}
          <section id="about" className="bg-white dark:bg-black pt-8">
          <div className="gap-16 items-center py-8 px-4 mx-auto max-w-screen-xl lg:grid lg:grid-cols-2 lg:py-8 lg:px-6">
            <div className="font-light text-gray-500 sm:text-lg dark:text-gray-400">
              <h2 className="mb-4 text-5xl tracking-tight font-extrabold text-gray-900 dark:text-white">
                About Me              </h2>
              <p className="mb-4 text-3xl">
              I've dedicated my career to finding the vulnerabilities that others miss. My journey began with CTF competitions and evolved into a full-time commitment to making digital spaces more secure.
              </p>
              <p className="text-xl">
             My approach combines creative problem-solving with rigorous methodology, ensuring no stone is left unturned in the pursuit of robust security.
              </p>
              <a href="#" className="inline-flex mt-8 items-center justify-center px-5 py-4 text-base font-medium text:3xl text-center text-gray-900 border-4 border-blue-300  hover:bg-blue-100 focus:ring-4 focus:ring-gray-100 dark:text-white dark:border-blue-700 dark:hover:bg-blue-700 dark:focus:ring-gray-800"
          >
            Download C.V.
          </a>
            </div>
            <div className="grid grid-cols-2 gap-4 mt-8">
            <img
              className="w-full transition-all duration-300 hover:saturate-150 hover:brightness-75 hover:hue-rotate-15"
              src="./assets/images/office-long-2.png"
              alt="office content 1"
            />
            <img
              className="mt-4 w-full lg:mt-10 transition-all duration-300 hover:saturate-150 hover:brightness-75 hover:hue-rotate-15"
              src="./assets/images/office-long-1.png"
              alt="office content 2"
            />
          </div>
          </div>
          <div className="max-w-screen-xl px-4 pb-8 mx-auto text-center lg:pb-16 lg:px-6">
            <figure className="max-w-screen-md mx-auto">
              <svg
                className="h-12 mx-auto mb-3 text-gray-400 dark:text-gray-600"
                viewBox="0 0 24 27"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M14.017 18L14.017 10.609C14.017 4.905 17.748 1.039 23 0L23.995 2.151C21.563 3.068 20 5.789 20 8H24V18H14.017ZM0 18V10.609C0 4.905 3.748 1.038 9 0L9.996 2.151C7.563 3.068 6 5.789 6 8H9.983L9.983 18L0 18Z"
                  fill="currentColor"
                />
              </svg>
              <blockquote className="transform transition-all duration-300 hover:scale-125">
              <p className="text-2xl font-medium py-8 text-gray-900 dark:text-white">
                "Working with HAK3R transformed our security posture completely. Their methodical approach to penetration testing uncovered critical vulnerabilities that our internal team had missed for months. What sets them apart isn't just their technical expertise, but their ability to communicate complex security concepts in a way that resonates with us."
              </p>
            </blockquote>
              <figcaption className="flex items-center justify-center mt-6 space-x-3">
              <img
                className="w-6 h-6 rounded-full transition-opacity duration-300 hover:opacity-70"
                src="./assets/images/michael-gouch.png"
                alt="profile picture"
              />
                <div className="flex items-center divide-x-2 divide-gray-500 dark:divide-gray-700">
                  <div className="pr-3 font-medium text-gray-900 dark:text-white">
                    John Doe
                  </div>
                  <div className="pl-3 text-sm font-light text-gray-500 dark:text-gray-400">
                    CEO at Google
                  </div>
                </div>
              </figcaption>
            </figure>
          </div>
        </section>
        <section id="contact" className="bg-white dark:bg-black">
          <div className="gap-8 items-center py-8 px-4 mx-auto max-w-screen-xl xl:gap-16 md:grid md:grid-cols-2 sm:py-16 lg:px-6">
            <img
              className="w-full transition-opacity duration-300 hover:opacity-70"
              src="./assets/images/data.png"
              alt="dashboard image"
            />
            <div className="mt-4 md:mt-0">
              <h2 className="mb-4 text-4xl tracking-tight font-extrabold text-gray-900 dark:text-white">
              Ready to Strengthen Your Security Posture?
              </h2>
              <p className="mb-6 font-light text-gray-500 text-xl lg:text-2xl dark:text-gray-400">
              Let's connect and discuss how I can help identify vulnerabilities in your systems before malicious actors do.
              </p>
              <p className="mb-6 font-light text-gray-500 text-xl lg:text-2xl dark:text-gray-400">Whether you need penetration testing, security consultation, or vulnerability assessments, I'm here to provide expert guidance that fits your organization's unique needs. 
              </p>
            </div>
          </div>
        </section>
        {/* #### CONTACT SECTION #### */}
        <section className="bg-white dark:bg-black transition-all duration-300 hover:scale-105">
          <div className="py-8 lg:py-16 px-4 mx-auto max-w-screen-md">
            <h2 className="mb-4 text-4xl tracking-tight font-extrabold text-center text-gray-900 dark:text-white">
            Book a consultation today – your security is my priority
            </h2>
            <p className="mb-8 lg:mb-16 font-light text-center text-gray-500 dark:text-gray-400 text-xl lg:text-2xl">
            Protect your digital assets and maintain customer trust with proactive security testing.
            </p>
            <form action="#" className="space-y-8">
            <div>
                <label htmlFor="email" className="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300">
                  Your name
                </label>
                <input
                  type="text"
                  id="name"
                  className="shadow-sm bg-gray-50 border-4 border-blue-300 text-gray-900 text-sm  focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-black dark:border-blue-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500 dark:shadow-sm-light"
                  placeholder="John Doe"
                  required
                />
              </div>
              <div>
                <label htmlFor="email" className="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300">
                  Your email
                </label>
                <input
                  type="email"
                  id="email"
                  className="shadow-sm bg-gray-50 border-4 border-blue-300 text-gray-900 text-sm  focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-black dark:border-blue-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500 dark:shadow-sm-light"
                  placeholder="name@company.com"
                  required
                />
              </div>
              <div>
                <label htmlFor="subject" className="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300">
                  Subject
                </label>
                <input
                  type="text"
                  id="subject"
                  className="block p-3 w-full text-sm text-gray-900 bg-gray-50  border-4 border-blue-300 shadow-sm focus:ring-primary-500 focus:border-primary-500 dark:bg-black dark:border-blue-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500 dark:shadow-sm-light"
                  placeholder="Let us know how we can help you"
                  required
                />
              </div>
              <div className="sm:col-span-2">
                <label htmlFor="message" className="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-400">
                  Your message
                </label>
                <textarea
                  id="message"
                  rows={6}
                  className="block p-2.5 w-full text-sm text-gray-900 bg-gray-50  shadow-sm border-4 border-blue-300 focus:ring-primary-500 focus:border-primary-500 dark:bg-black dark:border-blue-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500"
                  placeholder="Leave a comment..."
                ></textarea>
              </div>
              <button
                type="submit"
                className="py-3 px-5 text-lx font-medium text-center text-white bg-blue-600 hover:bg-blue-700 border-2 border-blue-600 rounded-none sm:w-fit focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:border-blue-600 dark:focus:ring-blue-800"
              >
                Send message
              </button>
            </form>
          </div>
        </section>
      </main>
      <Footer />
    </>
  );
};

export default App;
