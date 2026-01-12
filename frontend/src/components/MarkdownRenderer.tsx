import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface MarkdownRendererProps {
  content: string;
  className?: string;
}

export const MarkdownRenderer = ({ content, className = '' }: MarkdownRendererProps) => {
  return (
    <div className={`prose prose-sm max-w-none ${className}`}>
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          // Customize heading styles
          h1: ({ ...props }) => <h1 className="text-2xl font-bold text-gray-800 mt-6 mb-4" {...props} />,
          h2: ({ ...props }) => <h2 className="text-xl font-bold text-gray-800 mt-5 mb-3" {...props} />,
          h3: ({ ...props }) => <h3 className="text-lg font-semibold text-gray-800 mt-4 mb-2" {...props} />,
          h4: ({ ...props }) => <h4 className="text-base font-semibold text-gray-800 mt-3 mb-2" {...props} />,
          // Customize paragraph styles
          p: ({ ...props }) => <p className="text-gray-700 mb-3 leading-relaxed" {...props} />,
          // Customize list styles
          ul: ({ ...props }) => <ul className="list-disc list-inside mb-3 text-gray-700 space-y-1" {...props} />,
          ol: ({ ...props }) => <ol className="list-decimal list-inside mb-3 text-gray-700 space-y-1" {...props} />,
          li: ({ ...props }) => <li className="ml-4" {...props} />,
          // Customize strong/bold text
          strong: ({ ...props }) => <strong className="font-semibold text-gray-800" {...props} />,
          // Customize emphasis/italic text
          em: ({ ...props }) => <em className="italic text-gray-700" {...props} />,
          // Customize code blocks
          code: ({ inline, ...props }: { inline?: boolean; [key: string]: any }) => 
            inline ? (
              <code className="bg-gray-100 px-1.5 py-0.5 rounded text-sm font-mono text-gray-800" {...props} />
            ) : (
              <code className="block bg-gray-100 p-3 rounded text-sm font-mono text-gray-800 overflow-x-auto mb-3" {...props} />
            ),
          pre: ({ ...props }) => <pre className="bg-gray-100 p-3 rounded overflow-x-auto mb-3" {...props} />,
          // Customize blockquotes
          blockquote: ({ ...props }) => (
            <blockquote className="border-l-4 border-primary-300 pl-4 italic text-gray-600 my-3" {...props} />
          ),
          // Customize links
          a: ({ ...props }) => (
            <a className="text-primary-600 hover:text-primary-700 underline" {...props} />
          ),
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
};
