import React from 'react';

interface BlogPostProps {
  title: string;
  author: string;
  date: string;
  children: React.ReactNode;
}

const BlogPost: React.FC<BlogPostProps> = ({ title, author, date, children }) => {
  return (
    <article className="bg-gray-900/50 border border-cyan-500/30 rounded-lg p-6 md:p-8 shadow-lg shadow-cyan-500/10 backdrop-blur-sm animate-fadeIn mb-8">
      <header>
        <h2 className="text-3xl md:text-4xl font-bold text-cyan-300 drop-shadow-[0_0_8px_theme(colors.cyan.400)] tracking-wide mb-2">
          {title}
        </h2>
        <div className="text-sm text-gray-500 mb-4 tracking-wider">
          <span>By {author}</span> | <span>{date}</span>
        </div>
      </header>
      <div className="text-gray-300 leading-relaxed">
        {children}
      </div>
      <footer className="mt-6">
        <a
          href="#"
          className="inline-block px-6 py-2 border border-cyan-400/50 text-cyan-400 rounded-sm uppercase tracking-widest text-sm font-semibold
                     hover:bg-cyan-400 hover:text-black hover:shadow-md hover:shadow-cyan-400/40
                     transition-all duration-300 ease-in-out transform hover:scale-105"
        >
          Decrypt Transmission
        </a>
      </footer>
    </article>
  );
};

export default BlogPost;
