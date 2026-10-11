import React from 'react';
import { motion } from 'framer-motion';

const container = {
  initial: {},
  animate: {
    transition: { staggerChildren: 0.045, delayChildren: 0.08 }
  },
};

const word = {
  initial: { opacity: 0, y: 16 },
  animate: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.4, ease: [0.22, 1, 0.36, 1] }
  },
};

export default function AnimatedText({ text, tag = 'span', className }) {
  const MotionTag = motion[tag];
  const words = text.split(' ');
  return (
    <MotionTag
      className={className}
      variants={container}
      initial="initial"
      animate="animate"
      style={{ display: 'inline-block' }}
    >
      {words.map((w, i) => (
        <motion.span
          key={i}
          variants={word}
          style={{ display: 'inline-block', marginRight: '0.28em' }}
        >
          {w}
        </motion.span>
      ))}
    </MotionTag>
  );
}