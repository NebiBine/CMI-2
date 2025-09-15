<template>
    <button class="interactive-btn">
      <!-- First state -->
      <div class="btn-front">
        <div class="dot"></div>
        <span class="label">{{ text }}</span>
      </div>
  
      <!-- Hover state -->
      <div class="btn-hover">
        <span class="label">{{ text }}</span>
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <path d="M5 12h14" />
          <path d="m12 5 7 7-7 7" />
        </svg>
      </div>
    </button>
  </template>
  
  <script setup lang="ts">
  interface Props {
    text?: string;
  }
  const props = withDefaults(defineProps<Props>(), {
    text: "Button",
  });
  </script>
  
  <style scoped>
  .interactive-btn {
    position: relative;
    display: inline-block;
    overflow: hidden;
    border: 2px solid #fff;
    border-radius: 9999px; /* rounded-full */
    padding: 0.6em 1.5em;
    font-weight: 600;
    font-size: 1rem;
    color: #fff;
    background: transparent;
    cursor: pointer;
    transition: background 0.3s ease, color 0.3s ease;
  }
  
  /* Animate background fill */
  .interactive-btn:hover {
    background: #000;
    color: #fff;
  }
  
  .btn-front,
  .btn-hover {
    display: flex;
    align-items: center;
    gap: 0.5em;
    transition: all 0.3s ease;
  }
  
  .btn-front {
    opacity: 1;
    transform: translateX(0);
  }
  
  .btn-hover {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%) translateX(50px);
    opacity: 0;
  }
  
  .interactive-btn:hover .btn-front {
    opacity: 0;
    transform: translateX(-50px);
  }
  
  .interactive-btn:hover .btn-hover {
    opacity: 1;
    transform: translate(-50%, -50%) translateX(0);
  }
  
  .dot {
    width: 8px;
    height: 8px;
    background: #fff;
    border-radius: 4px;
    transition: transform 0.3s ease;
  }
  
  .interactive-btn:hover .dot {
    transform: scale(1.2);
  }
  </style>
  