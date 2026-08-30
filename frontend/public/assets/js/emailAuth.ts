import { useState, useEffect } from "react";



export function emailAuth() {

  const [isVerified, setIsVerified] = useState(false);
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);
  const [authStep, setAuthStep] = useState("email");
  const [authEmail, setAuthEmail] = useState("");
  const [authCode, setAuthCode] = useState("");
  const [authLoading, setAuthLoading] = useState(false);
  const [authMessage, setAuthMessage] = useState("");
  
  useEffect(() => {
    fetch("http://localhost:8000/auth/status", {
      credentials: "include"
    })
      .then(res => res.json())
      .then(data => {
        if (data.verified) {
          setIsVerified(true);
          setIsAuthModalOpen(false);
        } else {
          setIsVerified(false);
          setIsAuthModalOpen(true);
        }
      })
      .catch(err => console.error("Error checking authentication: ", err));
  }, [])



  const handleRequestOtp = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!authEmail.trim() || !authEmail.includes("@")) {
      setAuthMessage("Please enter a valid email")
      return;
    }
    setAuthLoading(true);
    setAuthMessage("");

    try {
      const res = await fetch("http://localhost:8000/auth/request-code", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ email: authEmail }),
        credentials: "include"
      });
      const data = await res.json();

      if (data.error) {
        setAuthMessage(data.error);
      } else {
        setAuthStep("code");
        setAuthMessage("Code sent successfully! Please revise your recent emails")
      }
    } catch (err) {
      setAuthMessage("Connection error with the server. Please try again later")
    } finally {
      setAuthLoading(false)
    }
  };


  const handleVerifyOtp = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!authCode.trim()) {
      setAuthMessage("Introduce the verification code");
      return;
    }
    setAuthLoading(true);
    setAuthMessage("");

    try {
      const res = await fetch("http://localhost:8000/auth/verify-code", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ code: authCode }),
        credentials: "include"
      });
      const data = await res.json();

      if (data.error) {
        setAuthMessage(data.error);
      } else {
        setAuthMessage("Email verification successfull!")
        setIsVerified(true);
        setTimeout(() => {
          setIsAuthModalOpen(false);
          setAuthStep("email");
          setAuthCode("");
          setAuthEmail("");
          setAuthMessage("");
        }, 1200);
      }
    } catch (e) {
      setAuthMessage("Error verifying the code");
    } finally {
      setAuthLoading(false);
    }
  };

  return {
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
  };

}
