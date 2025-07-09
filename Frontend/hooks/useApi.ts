"use client"

// Custom React hooks for API integration
import { useState, useEffect } from "react"
import { DatabaseService } from "@/lib/api"

export const useBusinessIdeas = (userId: string) => {
  const [ideas, setIdeas] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!userId) return;

    const fetchIdeas = async () => {
      try {
        const res = await fetch(`http://127.0.0.1:8000/api/ideas/user/${userId}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
            "Content-Type": "application/json",
          },
        });
        const data = await res.json();
        setIdeas(data);
      } catch (err) {
        console.error("Failed to fetch user ideas:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchIdeas();
  }, [userId]);

  return { ideas, loading };
};


export function useSchemeMatches(userId: string) {
  const [matches, setMatches] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function fetchMatches() {
      try {
        const schemeMatches = await DatabaseService.getSchemeMatches(userId)
        setMatches(schemeMatches)
      } catch (err) {
        console.error("Failed to fetch scheme matches:", err)
      } finally {
        setLoading(false)
      }
    }

    if (userId) {
      fetchMatches()
    }
  }, [userId])

  return { matches, loading }
}

export function useLearningProgress(userId: string) {
  const [progress, setProgress] = useState({})
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function fetchProgress() {
      try {
        const userProgress = await DatabaseService.getUserProgress(userId)
        setProgress(userProgress)
      } catch (err) {
        console.error("Failed to fetch learning progress:", err)
      } finally {
        setLoading(false)
      }
    }

    if (userId) {
      fetchProgress()
    }
  }, [userId])

  const updateProgress = async (moduleId: string, progressValue: number) => {
    try {
      await DatabaseService.updateLearningProgress(userId, moduleId, progressValue)
      setProgress((prev) => ({
        ...prev,
        [moduleId]: progressValue,
      }))
    } catch (err) {
      console.error("Failed to update progress:", err)
    }
  }

  return { progress, loading, updateProgress }
}
