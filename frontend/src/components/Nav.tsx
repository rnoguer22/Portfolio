import React, { useState, useEffect } from "react";
import { useNavigate, useLocation, Link } from "react-router-dom";
import { Navbar } from "flowbite-react";
import { DarkThemeToggle } from "flowbite-react";



const Nav: React.FC = () => {
  const [isScrolled, setIsScrolled] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  // useEffect is a hook use for loading things when the 'Nav' component is initialized for the first time 
  useEffect(() => {
    
    // We check if the user's browser preference is in dark mode 
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    
    // Then we define a function to set the tag 'dark' depending on the user's browser preference 
    // This allows us to manage the dark / light mode in our website with Tailwind
    const handleThemeChange = (e: MediaQueryListEvent | MediaQueryList) => {
      if (e.matches) {
        // System prefers dark mode
        document.documentElement.classList.add('dark');
      } else {
        // System prefers light mode
        document.documentElement.classList.remove('dark');
      }
    };
    // Apply the theme  
    handleThemeChange(mediaQuery);

    // Listen for system theme changes
    mediaQuery.addEventListener('change', handleThemeChange);

    // Scroll handler. This changes the navbar dimensions depending on the y-scroll 
    const handleScroll = () => {
      if (window.scrollY > 50) {
        setIsScrolled(true);
      } else {
        setIsScrolled(false);
      }
    };

    window.addEventListener('scroll', handleScroll);
    
    // When the Nav component is destroyed the listeners are eliminated for preventing memory leaks 
    return () => {
      mediaQuery.removeEventListener('change', handleThemeChange);
      window.removeEventListener('scroll', handleScroll);
    };
  // By using [] below, it makes all these code to be executed just one time 
  }, []);



  // Function to handle nav clicks, making smooth transitions 
  const handleNavClick = (section: string) => {
    // If we are not in home, first we go to home 
    if (location.pathname !== '/') {
      navigate('/');
      // Then we wait home to load and we scroll to the destination
      setTimeout(() => {
        scrollToSection(section);
      }, 100);
    } else {
      // If we are already in home we just scroll into the section 
      scrollToSection(section);
    }
  };

  // Function to scroll to a section 
  const scrollToSection = (elementId: string) => {
    const element = document.getElementById(elementId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <Navbar 
    className={`fixed w-full transition-all duration-300 ${
      isScrolled 
        ? 'z-50 py-1 bg-white dark:bg-black shadow-lg md:bg-white md:dark:bg-black' 
        : 'z-50 py-4 bg-white dark:bg-black md:bg-transparent md:dark:bg-transparent'
    }`}
      fluid
    >
      <Navbar.Brand href="/">
        <img 
          src="./assets/images/portfolio.png" 
          className={`mr-3 transition-all duration-300 ${
            isScrolled ? 'h-5 sm:h-7' : 'h-6 sm:h-9'
          }`} 
          alt="Logo" 
        />
        <span className={`self-center whitespace-nowrap font-bold dark:text-white transition-all duration-300 ${
          isScrolled ? 'text-lg' : 'text-2xl'
        }`}>
          rnoguer
        </span>
      </Navbar.Brand>
      <div className="flex md:order-2">
        <DarkThemeToggle />
        <a
        href="https://github.com/rnoguer22"
        target="_blank"
        rel="noopener noreferrer"
        className={`hidden md:flex mx-3 bg-gray-800 hover:bg-gray-900 py-2 px-4 transition-all duration-300 flex items-center gap-2 ${
          isScrolled ? 'scale-90' : 'scale-100'
        }`}
      >
        <svg 
          className="w-6 h-6 text-gray-100" 
          aria-hidden="true" 
          xmlns="http://www.w3.org/2000/svg" 
          fill="currentColor" 
          viewBox="0 0 24 24"
        >
          <path 
            fillRule="evenodd" 
            d="M12.006 2a9.847 9.847 0 0 0-6.484 2.44 10.32 10.32 0 0 0-3.393 6.17 10.48 10.48 0 0 0 1.317 6.955 10.045 10.045 0 0 0 5.4 4.418c.504.095.683-.223.683-.494 0-.245-.01-1.052-.014-1.908-2.78.62-3.366-1.21-3.366-1.21a2.711 2.711 0 0 0-1.11-1.5c-.907-.637.07-.621.07-.621.317.044.62.163.885.346.266.183.487.426.647.71.135.253.318.476.538.655a2.079 2.079 0 0 0 2.37.196c.045-.52.27-1.006.635-1.37-2.219-.259-4.554-1.138-4.554-5.07a4.022 4.022 0 0 1 1.031-2.75 3.77 3.77 0 0 1 .096-2.713s.839-.275 2.749 1.05a9.26 9.26 0 0 1 5.004 0c1.906-1.325 2.74-1.05 2.74-1.05.37.858.406 1.828.101 2.713a4.017 4.017 0 0 1 1.029 2.75c0 3.939-2.339 4.805-4.564 5.058a2.471 2.471 0 0 1 .679 1.897c0 1.372-.012 2.477-.012 2.814 0 .272.18.592.687.492a10.05 10.05 0 0 0 5.388-4.421 10.473 10.473 0 0 0 1.313-6.948 10.32 10.32 0 0 0-3.39-6.165A9.847 9.847 0 0 0 12.007 2Z" 
            clipRule="evenodd"
          />
        </svg>
        <a href="https://github.com/rnoguer22" className="text-white font-medium">Github profile</a>
      </a>
        <button
          type="button"
          // onClick={() => scrollToSection('contact')}
          className={`text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-bold text-center mx-3 md:mr-0 z-10 transition-all duration-300 ${
            isScrolled ? 'text-sm px-3 py-1.5' : 'text-md px-4 py-2'
          }`}
        >
          Contact Me!
        </button>
        <Navbar.Toggle />
      </div>
      <Navbar.Collapse>
        {['home', 'services', 'about'].map((section) => (
          <button 
            key={section}
            onClick={() => handleNavClick(section)}
            className={`block pr-4 pl-3 border-b border-gray-100 text-gray-700 hover:bg-gray-50 font-bold dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white md:border-0 md:hover:bg-transparent md:hover:text-blue-700 md:dark:hover:bg-transparent md:dark:hover:text-white transition-all duration-300 ${
              isScrolled ? 'text-base text-3xl md:text-lg py-2' : 'text-3xl md:text-xl py-2.5'
            }`}
          >
            {section.charAt(0).toUpperCase() + section.slice(1)}
          </button>
        ))}
        <Link to="/agent" className="block pr-4 pl-3 border-b border-gray-100 text-gray-700 hover:bg-gray-50 font-bold dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white md:border-0 md:hover:bg-transparent md:hover:text-blue-700 md:dark:hover:bg-transparent md:dark:hover:text-white transition-all duration-300 text-3xl md:text-xl py-2.5">
          AI Demo
        </Link>
      </Navbar.Collapse>
    </Navbar>
  );
};

export default Nav;
