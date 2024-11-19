import React from 'react';
import { BrainCircuit, Server, Database, Code, Cloud, Zap } from 'lucide-react';

import ContactForm from './components/contact';

const Header = () => (
  <header className="bg-white shadow-sm">
    <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Cloudbend</h1>
        <nav className="space-x-4">
          <a href="#services" className="text-gray-600 hover:text-gray-900">Services</a>
          <a href="#contact" className="text-gray-600 hover:text-gray-900">Contact</a>
        </nav>
      </div>
    </div>
  </header>
);

const Hero = () => (
  <div className="bg-white">
    <div className="max-w-7xl mx-auto py-16 px-4 sm:py-24 sm:px-6 lg:px-8">
      <div className="text-center">
        <h1 className="text-4xl font-extrabold text-gray-900 sm:text-5xl sm:tracking-tight lg:text-6xl">
          Bend the cloud to your will
        </h1>
        <p className="mt-4 max-w-3xl mx-auto text-xl text-gray-500">
          We convert problems into solutions and ideas into reality.
        </p>
        <p className="mt-4 max-w-3xl mx-auto text-xl text-gray-500">
          Let us help you build the future.
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
      description: "Imbue intelligence into your workflows"
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
      description: "A solid foundation for the future of your business"
    },
    {
      icon: <Zap className="w-6 h-6 mb-4" />,
      title: "Rapid Development",
      description: "Fast iteration & focus on delivery"
    }
  ];

  return (
    <div id="services" className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
      <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
        {capabilities.map((capability, index) => (
          <div key={index} className="bg-white overflow-hidden shadow rounded-lg p-6">
            <div className="text-gray-900">{capability.icon}</div>
            <h3 className="text-lg font-medium text-gray-900">{capability.title}</h3>
            <p className="mt-2 text-base text-gray-500">{capability.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

const Contact = () => (
  <div id="contact" className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
    <div className="max-w-xl mx-auto">
      <h2 className="text-3xl font-extrabold text-gray-900 text-center mb-8">Contact Us</h2>
      <ContactForm />
    </div>
  </div>
);

const Footer = () => (
  <footer className="bg-white mt-12">
    <div className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
      <div className="text-center text-gray-500">
        <p>&copy; 2024 Cloudbend. All rights reserved.</p>
      </div>
    </div>
  </footer>
);

const Website = () => (
  <div className="min-h-screen bg-gray-50">
    <Header />
    <Hero />
    <Capabilities />
    <Contact />
    <Footer />
  </div>
);

export default Website;