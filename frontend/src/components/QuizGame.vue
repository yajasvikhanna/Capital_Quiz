<template>
  <div class="quiz-container">
    <div v-if="loading" class="loading">
      <p>Loading question...</p>
    </div>
    
    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
      <button @click="loadNewQuestion" class="btn btn-secondary">Try Again</button>
    </div>
    
    <div v-else class="quiz-content">
      <div class="question-section">
        <h2>{{ currentQuestion }}</h2>
        <div class="question-counter">
          Question {{ questionCount }}
        </div>
      </div>
      
      <div class="input-section">
        <input 
          v-model="userAnswer" 
          @keyup.enter="checkAnswer"
          :disabled="showResult"
          type="text" 
          placeholder="Enter the capital city..."
          class="answer-input"
          ref="answerInput"
        />
        <button 
          @click="checkAnswer" 
          :disabled="!userAnswer.trim() || showResult || checking"
          class="btn btn-primary"
        >
          {{ checking ? 'Checking...' : 'Check Answer' }}
        </button>
      </div>
      
      <div v-if="showResult" class="result-section">
        <div :class="['result', { 'correct': lastResult.is_correct, 'incorrect': !lastResult.is_correct }]">
          <div class="result-icon">
            {{ lastResult.is_correct ? '✅' : '❌' }}
          </div>
          <div class="result-text">
            <h3>{{ lastResult.is_correct ? 'Correct!' : 'Incorrect!' }}</h3>
            <p v-if="!lastResult.is_correct">
              The correct answer is: <strong>{{ lastResult.correct_answer }}</strong>
            </p>
            <p v-else>
              Great job! {{ lastResult.correct_answer }} is correct!
            </p>
          </div>
        </div>
        
        <button @click="loadNewQuestion" class="btn btn-secondary">
          Next Question
        </button>
      </div>
      
      <div class="stats">
        <div class="stat">
          <span class="stat-label">Correct:</span>
          <span class="stat-value">{{ stats.correct }}</span>
        </div>
        <div class="stat">
          <span class="stat-label">Incorrect:</span>
          <span class="stat-value">{{ stats.incorrect }}</span>
        </div>
        <div class="stat">
          <span class="stat-label">Accuracy:</span>
          <span class="stat-value">{{ accuracy }}%</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'QuizGame',
  data() {
    return {
      currentQuestion: '',
      currentCountry: null,
      userAnswer: '',
      showResult: false,
      lastResult: null,
      loading: false,
      checking: false,
      error: null,
      questionCount: 0,
      stats: {
        correct: 0,
        incorrect: 0
      }
    }
  },
  computed: {
    accuracy() {
      const total = this.stats.correct + this.stats.incorrect
      if (total === 0) return 0
      return Math.round((this.stats.correct / total) * 100)
    }
  },
  mounted() {
    this.loadNewQuestion()
  },
  methods: {
    async loadNewQuestion() {
      this.loading = true
      this.error = null
      this.showResult = false
      this.userAnswer = ''
      
      try {
        const response = await axios.get('/api/question/')
        this.currentQuestion = response.data.question
        this.currentCountry = response.data.country
        this.questionCount++
        
        // Focus on input after loading
        this.$nextTick(() => {
          if (this.$refs.answerInput) {
            this.$refs.answerInput.focus()
          }
        })
      } catch (error) {
        console.error('Error loading question:', error)
        this.error = 'Failed to load question. Please try again.'
      } finally {
        this.loading = false
      }
    },
    
    async checkAnswer() {
      if (!this.userAnswer.trim() || !this.currentCountry) return
      
      this.checking = true
      
      try {
        const response = await axios.post('/api/check-answer/', {
          country_id: this.currentCountry.id,
          user_answer: this.userAnswer.trim()
        })
        
        this.lastResult = response.data
        this.showResult = true
        
        // Update stats
        if (response.data.is_correct) {
          this.stats.correct++
        } else {
          this.stats.incorrect++
        }
        
      } catch (error) {
        console.error('Error checking answer:', error)
        this.error = 'Failed to check answer. Please try again.'
      } finally {
        this.checking = false
      }
    }
  }
}
</script>

<style scoped>
.quiz-container {
  min-height: 400px;
}

.loading, .error {
  text-align: center;
  padding: 40px;
}

.error {
  color: #e74c3c;
}

.question-section {
  text-align: center;
  margin-bottom: 30px;
}

.question-section h2 {
  font-size: 1.8rem;
  color: #2c3e50;
  margin-bottom: 10px;
}

.question-counter {
  display: inline-block;
  background: #ecf0f1;
  padding: 5px 15px;
  border-radius: 20px;
  font-size: 0.9rem;
  color: #7f8c8d;
}

.input-section {
  display: flex;
  gap: 15px;
  margin-bottom: 30px;
  align-items: center;
}

.answer-input {
  flex: 1;
  padding: 12px 15px;
  border: 2px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.answer-input:focus {
  outline: none;
  border-color: #667eea;
}

.answer-input:disabled {
  background-color: #f8f9fa;
  cursor: not-allowed;
}

.btn {
  padding: 12px 20px;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
  font-weight: 500;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary {
  background-color: #667eea;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background-color: #5a6fd8;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.btn-secondary:hover:not(:disabled) {
  background-color: #5a6268;
}

.result-section {
  text-align: center;
  margin-bottom: 30px;
}

.result {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  padding: 20px;
  border-radius: 10px;
  margin-bottom: 20px;
}

.result.correct {
  background-color: #d4edda;
  border: 1px solid #c3e6cb;
  color: #155724;
}

.result.incorrect {
  background-color: #f8d7da;
  border: 1px solid #f5c6cb;
  color: #721c24;
}

.result-icon {
  font-size: 2rem;
}

.result-text h3 {
  margin: 0 0 10px 0;
  font-size: 1.5rem;
}

.result-text p {
  margin: 0;
  font-size: 1.1rem;
}

.stats {
  display: flex;
  justify-content: center;
  gap: 30px;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.stat {
  text-align: center;
}

.stat-label {
  display: block;
  font-size: 0.9rem;
  color: #6c757d;
  margin-bottom: 5px;
}

.stat-value {
  display: block;
  font-size: 1.5rem;
  font-weight: bold;
  color: #2c3e50;
}

@media (max-width: 600px) {
  .input-section {
    flex-direction: column;
  }
  
  .stats {
    flex-direction: column;
    gap: 15px;
  }
  
  .result {
    flex-direction: column;
    text-align: center;
  }
}
</style>