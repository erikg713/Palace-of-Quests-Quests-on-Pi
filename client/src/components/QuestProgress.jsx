import React from 'react';
import PropTypes from 'prop-types';
import styles from './QuestProgress.module.css';

/**
 * QuestProgress - Displays a progress bar with percentage.
 *
 * @param {Object} props
 * @param {number} props.progress - The progress percentage (0-100)
 */
function QuestProgress({ progress }) {
  // Clamp progress between 0 and 100
  const safeProgress = Math.max(0, Math.min(progress, 100));
  const isComplete = safeProgress === 100;

  return (
    <div className={styles.container}>
      <div
        className={styles.barBackground}
        aria-label="Quest Progress"
        role="progressbar"
        aria-valuenow={safeProgress}
        aria-valuemin={0}
        aria-valuemax={100}
      >
        <div
          className={isComplete ? styles.barFillComplete : styles.barFill}
          style={{ width: `${safeProgress}%` }}
        />
      </div>
      <span className={styles.progressText}>
        {safeProgress}% completed
      </span>
    </div>
  );
}

QuestProgress.propTypes = {
  progress: PropTypes.number.isRequired,
};

export default QuestProgress;
