import { defineStore } from 'pinia'

export const useRecommendationsStore = defineStore('recommendations', {
  state: () => ({
    recommendations: [],
    userId: null,
    selectedGenres: []
  }),
  actions: {
    setRecommendations(data) {
      this.recommendations = data.recommendations
      this.userId = data.user_id
      this.selectedGenres = data.selected_genres
    }
  }
})