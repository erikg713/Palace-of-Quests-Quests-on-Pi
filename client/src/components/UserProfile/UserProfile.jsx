import React from 'react';
import styles from './UserProfile.module.css';

const UserProfile = ({ name, bio, profilePicture, onEdit, onDelete }) => {
  return (
    <div className={styles.userProfile}>
      <div className={styles.profilePicture}>
        <img src={profilePicture} alt={`${name}'s profile`} />
      </div>
      <h2 className={styles.userName}>{name}</h2>
      <p className={styles.userBio}>{bio}</p>
      <div className={styles.actionButtons}>
        <button className={styles.editButton} onClick={onEdit}>
          Edit
        </button>
        <button className={styles.deleteButton} onClick={onDelete}>
          Delete
        </button>
      </div>
    </div>
  );
};

export default UserProfile;
