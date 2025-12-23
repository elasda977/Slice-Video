import api from './axios'

export const videoApi = {
  // Get all videos
  getVideos: () => api.get('/videos'),

  // Get single video
  getVideo: (id) => api.get(`/videos/${id}`),

  // Delete video
  deleteVideo: (id) => api.delete(`/videos/${id}`),

  // Upload video file
  uploadVideo: (file, onProgress) => {
    const formData = new FormData()
    formData.append('file', file)

    return api.post('/videos/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (progressEvent) => {
        const percentCompleted = Math.round(
          (progressEvent.loaded * 100) / progressEvent.total
        )
        if (onProgress) onProgress(percentCompleted)
      },
    })
  },

  // Start conversion
  convertVideo: (videoName, segmentDuration = 6) =>
    api.post('/convert', {
      video_name: videoName,
      segment_duration: segmentDuration,
    }),

  // Get conversion progress
  getProgress: (videoName) => api.get(`/progress/${videoName}`),

  // Cancel conversion
  cancelConversion: (videoName) => api.post(`/convert/cancel/${videoName}`),

  // Get server status
  getServerStatus: () => api.get('/status'),

  // Cleanup all videos
  cleanupAll: () => api.delete('/cleanup'),
}

export const authApi = {
  // Register
  register: (username, email, password) =>
    api.post('/auth/register', { username, email, password }),

  // Login
  login: (username, password) =>
    api.post('/auth/login', { username, password }),

  // Get current user
  getCurrentUser: () => api.get('/auth/me'),
}
