import React, { useState } from 'react';

const VideoForm = ({ setVideoUrl }) => {
  const [formData, setFormData] = useState({
    title: '',
    useAI: 'yes',
    theme: '',
    content: '',
  });

  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setVideoUrl(null); // Clear previous video

    try {
      const response = await fetch('https://shortsyai-production-6337.up.railway.app/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      const data = await response.json();
      if (data.video_url) {
        const fullUrl = `https://shortsyai-production-6337.up.railway.app${data.video_url}`;
        setVideoUrl(fullUrl);
      } else {
        alert(data.message || '❌ Error: No video URL returned');
      }
    } catch (err) {
      console.error(err);
      alert('❌ Video generation failed');
    }

    setLoading(false);
  };

  return (
    <div className="flex flex-col items-center">
      <form
        onSubmit={handleSubmit}
        className="mt-16 bg-white/20 backdrop-blur-lg p-8 rounded-3xl shadow-xl border border-white/30 max-w-xl w-full text-white"
      >
        <h2 className="text-2xl font-semibold mb-6">🎬 Create Your AI Video</h2>

        <label className="block mb-3">
          <span className="font-medium">Video Title</span>
          <input
            type="text"
            name="title"
            value={formData.title}
            onChange={handleChange}
            required
            className="w-full mt-1 px-4 py-2 rounded-lg text-black"
          />
        </label>

        <label className="block mb-4">
          <span className="font-medium">Use AI to generate content?</span>
          <select
            name="useAI"
            value={formData.useAI}
            onChange={handleChange}
            className="w-full mt-1 px-4 py-2 rounded-lg text-black"
          >
            <option value="yes">Yes</option>
            <option value="no">No</option>
          </select>
        </label>

        {formData.useAI === 'yes' ? (
          <label className="block mb-4">
            <span className="font-medium">Theme of the Video</span>
            <input
              type="text"
              name="theme"
              value={formData.theme}
              onChange={handleChange}
              className="w-full mt-1 px-4 py-2 rounded-lg text-black"
              required
            />
          </label>
        ) : (
          <label className="block mb-4">
            <span className="font-medium">Content of the Video</span>
            <textarea
              name="content"
              value={formData.content}
              onChange={handleChange}
              rows={4}
              className="w-full mt-1 px-4 py-2 rounded-lg text-black"
              required
            />
          </label>
        )}

        <button
          type="submit"
          className="w-full mt-6 bg-gradient-to-r from-blue-500 to-purple-600 text-white py-2 rounded-xl font-bold hover:scale-[1.02] transition-transform"
          disabled={loading}
        >
          {loading ? '⏳ Generating...' : '🚀 Generate Video'}
        </button>
      </form>
    </div>
  );
};

export default VideoForm;
