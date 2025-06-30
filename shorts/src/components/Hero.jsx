import phone from '../assets/phone.png'; // Update this path if needed
import React, { useState } from 'react';
import "@fontsource/poppins/700.css";
import background from '../assets/image.png';
import { motion, AnimatePresence } from 'framer-motion';
import VideoForm from './Videoform';
const Hero = () => {
  const [hovered, setHovered] = useState(false);
  const [videoUrl, setVideoUrl] = useState(null);  // 👈 Hold generated video URL

  return (
    <section
      className="relative w-full h-[150vh] flex items-center justify-center px-4 py-16 bg-cover bg-center"
      style={{ backgroundImage: `url(${background})` }}
    >
      <div
        className="relative max-w-7xl w-full flex items-center justify-center"
        onMouseEnter={() => setHovered(true)}
      >
        <AnimatePresence>
          {!hovered && (
            <motion.h1
              className="absolute z-0 top-0 text-[48px] md:text-[72px] font-extrabold leading-tight bg-gradient-to-r from-blue-500 to-purple-600 bg-clip-text text-transparent font-['Outfit'] text-center"
              initial={{ opacity: 1 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0, transition: { duration: 0.6 } }}
            >
              Unlocking AI Wonders
            </motion.h1>
          )}
        </AnimatePresence>

        <motion.div
          className="relative z-20 mt-5"
          animate={{ x: hovered ? -240 : 0 }}
          transition={{ duration: 1.2, ease: 'easeOut' }}
        >
          <img
            src={phone}
            alt="Phone UI"
            className="h-[600px] object-contain"
          />

          {/* 🎥 Dynamic Video Preview */}
          <div className="absolute top-[55px] left-[190.5px] w-[222px] h-[485px] overflow-hidden rounded-[24px] shadow-xl bg-black">
            {videoUrl ? (
              <>
                <video
                    src={videoUrl || "/demo.mp4"}
                    controls
                    autoPlay
                    playsInline
                    className="w-full h-full object-cover"
                />
                {videoUrl && (
                    <a
                    href={videoUrl}
                    download
                    className="absolute bottom-0 mt-5 left-1/2 transform -translate-x-1/2 bg-black text-white text-sm px-6 py-1 rounded-full shadow-md hover:bg-gray-500 transition"
                    >
                    ⬇ Download
                    </a>
                )}
                </>
            ) : (
              <p className="text-white text-center pt-32 text-sm">Waiting for video...</p>
            )}
          </div>
        </motion.div>

        <motion.div
          className="absolute left-1/2 z-10 ml-10 max-w-xl"
          initial={{ opacity: 0, x: 0 }}
          animate={hovered ? { opacity: 1, x: 20 } : { opacity: 0, x: 0 }}
          transition={{ duration: 1.2, ease: 'easeOut' }}
        >
          <h1 className="text-[40px] mt-20 md:text-[56px] font-extrabold leading-tight bg-gradient-to-r from-blue-500 to-purple-600 bg-clip-text text-transparent font-['Poppins']">
            Discover your<br />AI-powered future
          </h1>
          <p className="mt-4 text-white text-lg md:text-xl max-w-md">
            Let intelligence unfold before your eyes.
          </p>

          {/* ⬇️ Pass setVideoUrl to VideoForm */}
          <VideoForm setVideoUrl={setVideoUrl} />
        </motion.div>
      </div>
    </section>
  );
};

export default Hero;

