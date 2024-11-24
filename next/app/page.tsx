import React from 'react';
import { BrainCircuit, Server, Database, Code, Cloud, Zap } from 'lucide-react';
import ContactForm from './components/contact';
import { ModalButton } from './components/modal';

const Header = () => (
  <header>
    <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
      <div className="flex justify-between items-center">
        {/* next/image causes cls w/ svg src */}
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src="/logo.svg"
          width={200}
          height={200}
          alt="Cloudbend logo"
        />
        <div className="space-x-4">
          <ModalButton label="Contact">
            <ContactForm />
          </ModalButton>
        </div>
      </div>
    </div>
  </header>
);

const Hero = () => (
  <div className="container mx-auto px-4 pt-16 pb-8">
    <div className="max-w-7xl mx-auto pt-16 pb-8 lg:px-8">
      <div className="text-center">
        <h1 className="text-4xl font-extrabold text-white sm:text-5xl sm:tracking-tight lg:text-6xl">
          Bend the cloud to your will
        </h1>
        <p className="mt-4 max-w-3xl mx-auto text-xl text-white">
          Converting problems into solutions and ideas into reality.
        </p>
      </div>
    </div>
  </div>
);

const Capabilities = () => {
  const capabilities = [
    {
      icon: <Cloud className="w-6 h-6 mb-4" />,
      title: "Cloud Architecture",
      description: "Scalable and cost-efficient"
    },
    {
      icon: <BrainCircuit className="w-6 h-6 mb-4" />,
      title: "AI & Machine Learning",
      description: "Intelligence engineering"
    },
    {
      icon: <Zap className="w-6 h-6 mb-4" />,
      title: "Rapid Development",
      description: "Focus on delivery"
    },
    {
      icon: <Code className="w-6 h-6 mb-4" />,
      title: "Full-Stack Development",
      description: "End-to-end application development"
    },
    {
      icon: <Database className="w-6 h-6 mb-4" />,
      title: "Data Engineering",
      description: "Modern data architecture"
    },
    {
      icon: <Server className="w-6 h-6 mb-4" />,
      title: "Platform Engineering",
      description: "Solid foundations for the future of your business"
    }
  ];

  return (
    <div id="services" className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
      <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
        {capabilities.map((capability, index) => (
          <div key={index} className="bg-white/10 backdrop-blur rounded overflow-hidden shadow-xl p-8">
            <div className="text-white">{capability.icon}</div>
            <h3 className="text-lg font-medium text-white">{capability.title}</h3>
            <p className="mt-2 text-base text-white">{capability.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

const Contact = () => (
  <div id="contact" className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8 flex justify-center">
    <ModalButton className="bg-white rounded-lg px-4 py-2 text-gray-800" label="Let us help you build the future">
      <ContactForm />
    </ModalButton>
  </div>
);

const Footer = () => (
  <footer className="mt-12">
    <div className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
      <div className="text-center text-white">
        <p>&copy; 2024 Cloudbend. All rights reserved.</p>
      </div>
    </div>
  </footer>
);

const Website = () => (
  <div className="min-h-screen bg-gradient-to-br from-purple-600 via-blue-500 to-purple-800">
    <Header />
    <Hero />
    <Capabilities />
    <Contact />
    <Footer />
  </div>
);

export default Website;