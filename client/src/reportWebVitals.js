// reportWebVitals.js

/**
 * Reports web vitals metrics using the supplied callback.
 * Dynamically imports 'web-vitals' to avoid unnecessary bundle weight.
 * @param {Function} onPerfEntry - Callback function for handling metrics.
 */
const reportWebVitals = (onPerfEntry) => {
  if (typeof onPerfEntry === 'function') {
    import('web-vitals')
      .then(({ getCLS, getFID, getFCP, getLCP, getTTFB }) => {
        getCLS(onPerfEntry);      // Cumulative Layout Shift
        getFID(onPerfEntry);      // First Input Delay
        getFCP(onPerfEntry);      // First Contentful Paint
        getLCP(onPerfEntry);      // Largest Contentful Paint
        getTTFB(onPerfEntry);     // Time to First Byte
      })
      .catch((err) => {
        // Optionally, log or handle errors for diagnostics
        console.error('Failed to load web-vitals for reporting:', err);
      });
  }
};

export default reportWebVitals;
