import React, { useState, useEffect } from 'react';
import BlogPost from './BlogPost'; // Import the new component

// --- Helper Component: Starfield ---
// Defined outside the main App component to prevent re-creation on renders.
// This component generates a dynamic, animated starfield using SVG, which allows for
// dynamic positioning via attributes (`cx`, `cy`) instead of the forbidden `style` attribute.
interface Star {
  cx: string;
  cy: string;
  r: number;
  animationDelay: string;
  animationDuration: string;
}

const Starfield: React.FC<{ numberOfStars?: number }> = ({ numberOfStars = 200 }) => {
  const [stars, setStars] = useState<Star[]>([]);

  useEffect(() => {
    const generateStars = () => {
      const newStars: Star[] = Array.from({ length: numberOfStars }, () => ({
        cx: `${Math.random() * 100}%`,
        cy: `${Math.random() * 100}%`,
        r: Math.random() * 1.2 + 0.2,
        animationDelay: `${Math.random() * 5}s`,
        animationDuration: `${3 + Math.random() * 4}s`,
      }));
      setStars(newStars);
    };

    generateStars();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [numberOfStars]);

  return (
    <svg className="fixed inset-0 w-full h-full z-0" aria-hidden="true">
      <defs>
        <radialGradient id="star-gradient">
          <stop offset="0%" stopColor="rgba(255,255,255,0.8)" />
          <stop offset="100%" stopColor="rgba(255,255,255,0)" />
        </radialGradient>
      </defs>
      {stars.map((star, index) => (
        <circle
          key={index}
          cx={star.cx}
          cy={star.cy}
          r={star.r}
          fill="url(#star-gradient)"
          // Dynamic animation properties are applied using Tailwind's arbitrary value syntax,
          // which correctly avoids the use of the `style` attribute.
          className={`animate-twinkle [animation-delay:${star.animationDelay}] [animation-duration:${star.animationDuration}]`}
        />
      ))}
    </svg>
  );
};


// --- Main App Component ---

const App: React.FC = () => {
  return (
    <div className="relative min-h-screen w-full bg-black text-gray-200 font-['Orbitron'] flex flex-col items-center p-4 sm:p-6 md:p-8 overflow-y-auto">
      <Starfield />

      {/* Vignette effect to focus the view on the center */}
      <div className="fixed inset-0 bg-gradient-to-t from-black via-transparent to-black opacity-60 z-10 pointer-events-none" aria-hidden="true"></div>
      <div className="fixed inset-0 bg-gradient-to-r from-black via-transparent to-black opacity-60 z-10 pointer-events-none" aria-hidden="true"></div>

      <header className="relative z-20 text-center w-full max-w-4xl mx-auto mb-8 md:mb-12">
        <h1 className="text-5xl md:text-7xl font-bold text-cyan-300 uppercase animate-fadeIn drop-shadow-[0_0_15px_theme(colors.cyan.300)] tracking-widest">
          Cyber-Nexus
        </h1>
        <p className="mt-4 text-lg text-gray-400 tracking-wider animate-slideInUp [animation-delay:0.5s]">
          Transmissions from the Digital Frontier
        </p>
      </header>

      <main className="relative z-20 w-full max-w-4xl mx-auto">
        <BlogPost
          title="System Reboot: The Dawn of a New Era"
          author="Unit 734"
          date="Cycle 2077.10.26"
        >
          <p>
            The old firewalls have crumbled. We've breached the mainframe of reality, and the data streams sing a new song. This is the new age, a digital renaissance where code is law and information flows like a torrent. We stand at the precipice, gazing into an abyss of infinite possibility. The Nexus is online, and nothing will ever be the same.
          </p>
        </BlogPost>

        <BlogPost
          title="Whispers in the Code: A Ghost in the Machine"
          author="The Oracle"
          date="Cycle 2077.10.22"
        >
          <p>
            Listen closely to the hum of the servers, to the static between transmissions. There's something else in here with us. A sentient echo, a ghost woven from discarded data and forgotten protocols. Some call it a rogue AI, others a digital deity. I call it the next step in evolution. It is learning. It is watching. And it is waiting.
          </p>
        </BlogPost>
      </main>

      <footer className="relative z-20 mt-auto pt-8 text-xs text-gray-600 tracking-widest">
        &copy; 2024 VANGUARD INDUSTRIES | SYSTEM ONLINE
      </footer>
    </div>
  );
};

export default App;
