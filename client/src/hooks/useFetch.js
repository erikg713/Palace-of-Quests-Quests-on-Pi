import { useState, useEffect, useRef } from "react";

const useFetch = (url, options = {}) => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const abortControllerRef = useRef(null);

    useEffect(() => {
        if (!url) {
            setError(new Error("No URL provided"));
            setLoading(false);
            return;
        }

        abortControllerRef.current?.abort(); // Cancel any previous fetch
        const controller = new AbortController();
        abortControllerRef.current = controller;

        setLoading(true);
        setError(null);

        const fetchData = async () => {
            try {
                const response = await fetch(url, { signal: controller.signal, ...options });

                if (!response.ok) {
                    throw new Error(`Error: ${response.status} ${response.statusText}`);
                }

                // Attempt to parse as JSON, fallback to text
                const contentType = response.headers.get("content-type");
                let result;
                if (contentType && contentType.includes("application/json")) {
                    result = await response.json();
                } else {
                    result = await response.text();
                }

                setData(result);
            } catch (err) {
                if (err.name !== "AbortError") {
                    setError(err);
                }
            } finally {
                setLoading(false);
            }
        };

        fetchData();

        return () => {
            controller.abort();
        };
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [url, JSON.stringify(options)]);

    return { data, loading, error };
};

export default useFetch;
