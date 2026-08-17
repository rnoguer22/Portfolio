import Nav from "../components/Nav";
import Footer from "../components/Footer";
import "/public/assets/css/particles.css"; 



export default function Agent(){
  return (
    <div className="min-h-screen bg-black text-white flex flex-col">
      <Nav />
      <main className="flex-grow container mx-auto px-4 py-20">
        <h1 className="text-4xl font-bold mb-8">Agente de IA</h1>
        <div className="bg-gray-800 p-6 rounded-lg">
          <p>Futura interfaz con RAG y Agentes de IA</p>
        </div>
      </main>
      <Footer />
    </div>
  );
}
