import { useState, useEffect } from 'react';

export const useDarkMode = () => {
  const [isDarkMode, setIsDarkMode] = useState(false);

  useEffect(() => {
    // Check for saved preference or system preference
    const savedMode = localStorage.getItem('darkMode');
    if (savedMode) {
      const isDark = savedMode === 'true';
      setIsDarkMode(isDark);
      document.documentElement.classList.toggle('dark', isDark);
    } else {
      // Check system preference
      const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      setIsDarkMode(systemPrefersDark);
      document.documentElement.classList.toggle('dark', systemPrefersDark);
    }
  }, []);

  const toggleDarkMode = () => {
    const newMode = !isDarkMode;
    setIsDarkMode(newMode);
    localStorage.setItem('darkMode', String(newMode));
    // Only run on client
    if (typeof window !== 'undefined') {
      // Check for saved preference or system preference
      const savedMode = localStorage.getItem('darkMode');
      if (savedMode) {
        const isDark = savedMode === 'true';
        setIsDarkMode(isDark);
        document.documentElement.classList.toggle('dark', isDark);
      } else {
        // Check system preference
        const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        setIsDarkMode(systemPrefersDark);
        document.documentElement.classList.toggle('dark', systemPrefersDark);
      }
    }
  }, []);

  const toggleDarkMode = () => {
    const newMode = !isDarkMode;
    setIsDarkMode(newMode);
    if (typeof window !== 'undefined') {
      localStorage.setItem('darkMode', String(newMode));
      document.documentElement.classList.toggle('dark', newMode);
    }
  };

  return {
  const [isDarkMode, setIsDarkMode] = useState<boolean | undefined>(undefined);

  useEffect(() => {
    // Check for saved preference or system preference
    if (typeof window !== 'undefined') {
      const savedMode = localStorage.getItem('darkMode');
      if (savedMode !== null) {
        const isDark = savedMode === 'true';
        setIsDarkMode(isDark);
        document.documentElement.classList.toggle('dark', isDark);
      } else {
        // Check system preference
        const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        setIsDarkMode(systemPrefersDark);
        document.documentElement.classList.toggle('dark', systemPrefersDark);
      }
    }
  }, []);

  const toggleDarkMode = () => {
    if (typeof window !== 'undefined' && typeof isDarkMode === 'boolean') {
      const newMode = !isDarkMode;
      setIsDarkMode(newMode);
      localStorage.setItem('darkMode', String(newMode));
      document.documentElement.classList.toggle('dark', newMode);
    }
  };

  return {
    isDarkMode: isDarkMode ?? false,
    toggleDarkMode,
  };
};