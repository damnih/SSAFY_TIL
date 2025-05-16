import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import UserView from '@/views/UserView.vue'
import UserPosts from '@/components/UserPosts.vue'
import UserProfile from '@/components/UserProfile.vue'
import LoginView from '@/views/LoginView.vue'

// 상위 컴포넌트가 하위를 불러오듯이 import가 되어있당 


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      // 5173으로 들어오면 home을 보여주겠다.고 말하는 거임
      name: 'home',
      component: HomeView,
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
    {
      // 장고에서는 <int:pk> 이렇게 쓰던 거랑 같은 맥락
      // 근데 여긴 뷰잖아? 문법이 달라 
      // 뷰에서 변수랑 데이터랑 묶는 방법은 뭐지? (매개변수 만들어주는 방법)
      // => 바로 바인딩이다~! 
      // : 
      // 를 쓰는 게 바로 바인딩인거임
      // 변수명 앞에 그냥 무지성으로 : 적어주면 되는거임
      // 라우팅을 할 때도 이게 그냥 문자값이 아니라 묶고 싶으면 바인딩 해주면 된다는 거임~!  
      path: '/user/:id',
      // name: 'user',
      component: UserView,
      // 중첩된 라우팅 관리를 위해 이 안에(공통된 링크 주소를 가지고 있는 내부)
      // 안에 children 배열을 생성해주자 
      children: [
        { path: '', name: '', component: UserProfile},
        { path: '/profile', name: 'user-profile', component: UserProfile},
        { path: '/posts', name: 'user-post', component: UserPosts},
      ]
    },

// 이렇게 하나하나 만들어줄수도 있음 
// 그렇지만 중첩된 라우팅 관리를 위해 children 배열 생성해주자 
    // {
    //   path: '/user/:id/profile',
    //   name: 'profile',
    //   component: UserProfile
    // },
    // {
    //   path: '/user/:id/posts',
    //   name: 'posts',
    //   component: UserPosts
    // },
    {
      path: '/login',
      name: 'login',
      componenet: LoginView
    }

  ],
})

export default router
