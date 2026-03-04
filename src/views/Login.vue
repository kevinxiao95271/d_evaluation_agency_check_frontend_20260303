<template>
  <div class="login-container">
    <div class="login-box">
      <div class="login-header">
        <h2>机构考核评估系统</h2>
        <p>评委登录</p>
      </div>
      
      <el-form 
        ref="loginForm" 
        :model="form" 
        :rules="rules" 
        class="login-form"
        @submit.prevent="handleLogin"
      >
        <el-form-item prop="username">
          <el-input
            v-model="form.username"
            placeholder="请输入用户名"
            size="large"
            prefix-icon="User"
          />
        </el-form-item>
        
        <el-form-item prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="请输入密码"
            size="large"
            prefix-icon="Lock"
            @keyup.enter="handleLogin"
          />
        </el-form-item>
        
        <el-form-item>
          <el-button 
            type="primary" 
            size="large" 
            :loading="loading"
            @click="handleLogin"
            class="login-btn"
          >
            {{ loading ? '登录中...' : '登录' }}
          </el-button>
        </el-form-item>
      </el-form>
      
      <div class="login-tips">
        <h4>测试账号</h4>
        <div class="account-section">
          <p><strong>专家评委账号 (密码都是123456):</strong></p>
          <p>expert1, expert2, expert3, expert4, expert5...</p>
          <p><strong>大众评委账号 (密码都是123456):</strong></p>
          <p>public1, public2, public3, public4, public5...</p>
          <p><strong>管理员账号:</strong></p>
          <p>admin / admin123</p>
        </div>
        <div class="tip-note">
          <p>💡 提示：每个机构都有对应的专家和大众评委账号</p>
          <p>📊 可以用不同账号登录查看各自的评分进度</p>
          <p>🔍 <a href="/status" style="color: #409eff;">查看整体评分状态</a></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { judgeApi } from '../api'

export default {
  name: 'Login',
  setup() {
    const router = useRouter()
    const loginForm = ref(null)
    const loading = ref(false)
    
    const form = reactive({
      username: '',
      password: ''
    })
    
    const rules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' }
      ]
    }
    
    const handleLogin = async () => {
      try {
        await loginForm.value.validate()
        loading.value = true
        
        // 检查是否是管理员登录
        if (form.username === 'admin' && form.password === 'admin123') {
          const admin = {
            id: 0,
            name: '系统管理员',
            username: 'admin',
            type: 'ADMIN'
          }
          
          localStorage.setItem('admin', JSON.stringify(admin))
          ElMessage.success('管理员登录成功')
          router.push('/admin')
          return
        }
        
        // 评委登录
        const judge = await judgeApi.login(form.username, form.password)
        
        // 保存用户信息到localStorage
        localStorage.setItem('judge', JSON.stringify(judge))
        
        ElMessage.success('登录成功')
        router.push('/home')
        
      } catch (error) {
        console.error('登录失败:', error)
      } finally {
        loading.value = false
      }
    }
    
    return {
      loginForm,
      form,
      rules,
      loading,
      handleLogin
    }
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-box {
  width: 400px;
  padding: 40px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.login-header h2 {
  color: #333;
  margin-bottom: 10px;
  font-size: 24px;
}

.login-header p {
  color: #666;
  font-size: 14px;
}

.login-form {
  margin-bottom: 20px;
}

.login-btn {
  width: 100%;
}

.login-tips {
  text-align: center;
  font-size: 12px;
  color: #999;
  line-height: 1.5;
}

.login-tips h4 {
  color: #666;
  margin-bottom: 12px;
  font-size: 14px;
}

.account-section {
  background: #f8f9fa;
  padding: 12px;
  border-radius: 6px;
  margin-bottom: 12px;
  text-align: left;
}

.account-section p {
  margin: 6px 0;
}

.tip-note {
  background: #e6f7ff;
  padding: 8px;
  border-radius: 4px;
  border-left: 3px solid #1890ff;
}

.tip-note p {
  margin: 4px 0;
  font-size: 11px;
}
</style>