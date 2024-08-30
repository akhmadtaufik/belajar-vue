import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useTweet = defineStore('tweets', () => {
  const tweets = ref([
    {
      user: 'user_1',
      tweet: 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Dicta, praesentium?'
    },
    {
      user: 'user_2',
      tweet: 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Dicta, praesentium?'
    },
    {
      user: 'user_3',
      tweet: 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Dicta, praesentium?'
    },
    {
      user: 'user_4',
      tweet: 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Dicta, praesentium?'
    },
    {
      user: 'user_5',
      tweet: 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Dicta, praesentium?'
    }
  ])

  return {
    tweets
  }
})
