import { useState, useEffect } from 'react';

export const useGameState = () => {
  const [player, setPlayer] = useState(null);

  useEffect(() => {
    async function fetchPlayer() {
      const response = await fetch('/api/player');
      const data = await response.json();
      setPlayer(data);
    }
    fetchPlayer();
  }, []);

  return player;
};