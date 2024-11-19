<template>
  <div class="app-container">
    <header class="header">
      <h1>文档系统</h1>
    </header>
    <div class="main-content">
      <nav class="sidebar">
        <ul>
          <li v-for="folder in folders" 
              :key="folder" 
              @click="loadMarkdown(folder)"
              :class="{ active: currentFolder === folder }">
            {{ folder }}
          </li>
        </ul>
      </nav>
      <main class="content">
        <div v-html="renderedContent"></div>
      </main>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { marked } from 'marked'

export default {
  name: 'App',
  data() {
    return {
      folders: [],
      currentFolder: '',
      renderedContent: ''
    }
  },
  async created() {
    await this.loadFolders()
  },
  methods: {
    async loadFolders() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/folders')
        this.folders = response.data
      } catch (error) {
        console.error('加载文件夹失败:', error)
      }
    },
    async loadMarkdown(folder) {
      try {
          this.currentFolder = folder
          const response = await axios.get(`http://127.0.0.1:5000/api/file?folder=${folder}`)
          const content = response.data.content
          this.renderedContent = marked(content)  // 直接渲染处理后的内容
      } catch (error) {
          console.error('加载 Markdown 失败:', error)
      }
    }
  }
}
</script>

<style>
.app-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.header {
  background: #2c3e50;
  color: white;
  padding: 1rem;
}

.main-content {
  display: flex;
  flex: 1;
}

.sidebar {
  width: 250px;
  background: #f5f5f5;
  padding: 1rem;
  overflow-y: auto;
}

.sidebar ul {
  list-style: none;
  padding: 0;
}

.sidebar li {
  padding: 0.5rem;
  cursor: pointer;
  border-radius: 4px;
}

.sidebar li:hover {
  background: #e0e0e0;
}

.sidebar li.active {
  background: #42b983;
  color: white;
}

.content {
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
}

/* Markdown 样式 */
.content h1 { font-size: 2em; margin-bottom: 1rem; }
.content h2 { font-size: 1.5em; margin-bottom: 0.8rem; }
.content p { line-height: 1.6; margin-bottom: 1rem; }
.content img { max-width: 100%; }
</style>