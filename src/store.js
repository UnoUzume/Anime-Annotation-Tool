import { createStore } from 'vuex'

export default createStore({
  state() {
    return {
      maskCanvas_dic: {},
      colorCanvas_dic: {},
      colorWater_dic: {},
      //maskCanvas
      mCan_undoL: [],
      mCan_redoL: [],
      //colorCanvas
      cCan_undoL: [],
      cCan_redoL: [],
    }
  },
  getters: {
    getMCan: (state) => {
      return state.mCan_undoL[state.mCan_undoL.length - 1]
    },
    getCCan: (state) => {
      return state.cCan_undoL[state.cCan_undoL.length - 1]
    },
  },
  mutations: {
    canvasPushdo(state, cCanData, mCanData) {
      state.cCan_undoL.push(cCanData)
      state.mCan_undoL.push(mCanData)
      if (state.cCan_undoL.length > 100) {
        state.cCan_undoL = state.cCan_undoL.slice(50, -1)
        state.mCan_undoL = state.mCan_undoL.slice(50, -1)
      }
    },
    canvasUndo(state) {
      if (state.cCan_undoL.length <= 1) return
      state.cCan_redoL.push(state.cCan_undoL.pop())
      state.mCan_redoL.push(state.mCan_undoL.pop())
      if (state.cCan_redoL.length > 100) {
        state.cCan_redoL = state.cCan_redoL.slice(50, -1)
        state.mCan_redoL = state.mCan_redoL.slice(50, -1)
      }
    },
    canvasRedo(state) {
      if (state.cCan_redoL.length <= 0) return
      state.cCan_undoL.push(state.cCan_redoL.pop())
      state.mCan_undoL.push(state.mCan_redoL.pop())
      if (state.cCan_undoL.length > 100) {
        state.cCan_undoL = state.cCan_undoL.slice(50, -1)
        state.mCan_undoL = state.mCan_undoL.slice(50, -1)
      }
    },
  },
})
