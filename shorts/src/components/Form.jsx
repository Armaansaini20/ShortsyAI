import React, { useState } from 'react';
import axios from 'axios';

const Form = () => {
  const [title, setTitle] = useState('');
  const [option, setOption] = useState('yes');
  const [theme, setTheme] = useState('');
  const [content, setContent] = useState('');
  const [aiContent, setAIContent] = useState('');
  const [status, setStatus] = useState('');
  const [outputPath, setOutputPath] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setLoading(true);
    setStatus('');
    setOutputPath('');

    try {
      const payload = {
        title,
        useAI: option,
        theme,
        content: option === 'yes' ? aiContent || '' : content,
      };

      const res = await axios.post('http://127.0.0.1:8000/generate', payload);
      setStatus('Video generated successfully!');
      setOutputPath(res.data.output_path);
    } catch (err) {
      console.error(err);
      setStatus('❌ Error generating video');
    }

    setLoading(false);
  };

  return (
    <div>
      <input
        placeholder="Video Title"
        value={title}
        onChange={e => setTitle(e.target.value)}
      />

      <div>
        <label>
          <input
            type="radio"
            value="yes"
            checked={option === 'yes'}
            onChange={() => setOption('yes')}
          />
          Use AI
        </label>
        <label>
          <input
            type="radio"
            value="no"
            checked={option === 'no'}
            onChange={() => setOption('no')}
          />
          Manual
        </label>
      </div>

      {option === 'yes' && (
        <>
          <input
            placeholder="AI Prompt / Theme"
            value={theme}
            onChange={e => setTheme(e.target.value)}
          />
          <button
            onClick={async () => {
              setLoading(true);
              try {
                const res = await axios.post('http://127.0.0.1:8000/generate-ai', { theme });
                setAIContent(res.data.content);
              } catch (err) {
                console.error(err);
                setStatus('❌ Error generating AI content');
              }
              setLoading(false);
            }}
          >
            Generate Content
          </button>

          {aiContent && (
            <textarea
              value={aiContent}
              onChange={e => setAIContent(e.target.value)}
              rows={5}
            />
          )}
        </>
      )}

      {option === 'no' && (
        <textarea
          placeholder="Write your own content"
          value={content}
          onChange={e => setContent(e.target.value)}
          rows={5}
        />
      )}

      <br />
      <button onClick={handleSubmit} disabled={loading}>
        {loading ? 'Generating...' : 'Generate Video'}
      </button>

      {status && <p>{status}</p>}

      {outputPath && (
        <div style={{ marginTop: '20px' }}>
          <h4>✅ Preview:</h4>
          <video
            src={`http://127.0.0.1:8000/${outputPath}`}
            controls
            width="480"
          />
        </div>
      )}
    </div>
  );
};

export default Form;
