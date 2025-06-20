<template>
  <div id="app">
    <header>
      <h1>Sam's Capital Cities Quiz</h1>
      <p>World capitals! Knowledge Test</p>
    </header>
    <main>
      <QuizGame />
    </main>
  </div>
</template>

<script>
import QuizGame from "./components/QuizGame.vue";

export default {
  name: "App",
  components: {
    QuizGame,
  },
};
</script>

<style>
#app {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: "Segoe UI", Tahoma, Verdana, sans-serif;
}

header {
  text-align: center;
  margin-bottom: 30px;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 10px;
}

header h1 {
  margin: 0 0 10px 0;
  font-size: 2.5rem;
}

header p {
  margin: 0;
  font-size: 1.1rem;
  opacity: 0.9;
}

main {
  background: white;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 30px;
}
</style>
