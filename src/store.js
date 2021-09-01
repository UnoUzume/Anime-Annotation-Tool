import { createStore } from 'vuex'
import pako from 'pako'
let ClampedArray = Uint8ClampedArray
export default createStore({
  state() {
    return {
      mCan_dic: {},
      cCan_dic: {},
      cWater_dic: {},
      //maskCanvas
      mCan_undoL: [],
      mCan_redoL: [],
      //colorCanvas
      cCan_undoL: [],
      cCan_redoL: [],
    }
  },
  getters: {
    getCWater: (state) => (num) => {
      // console.time('inflate time')
      let uint8Array = ClampedArray.from(pako.inflate(state.cWater_dic[num]))
      // console.log('getCWater', state.cWater_dic[num], uint8Array)
      // console.timeEnd('inflate time')
      return new ImageData(uint8Array, 960, 540)
    },
    getMCan: (state) => (num) => {
      let uint8Array = ClampedArray.from(pako.inflate(state.mCan_dic[num]))
      // console.log('getMCan', state.cWater_dic[num], uint8Array)
      return new ImageData(uint8Array, 960, 540)
    },
    getCCan: (state) => (num) => {
      let uint8Array = ClampedArray.from(pako.inflate(state.cCan_dic[num]))
      // console.log('getCCan', state.cWater_dic[num], uint8Array)
      return new ImageData(uint8Array, 960, 540)
    },
    getUndoMCan: (state, getters) => {
      return state.mCan_undoL[state.mCan_undoL.length - 1]
    },
    getUndoCCan: (state) => {
      return state.cCan_undoL[state.cCan_undoL.length - 1]
    },
    toImgData: (state) => (array) => {
      let uint8Array = ClampedArray.from(pako.inflate(array))
      return new ImageData(uint8Array, 960, 540)
    },
  },
  mutations: {
    canvasPushdo(state, payload) {
      state.cCan_undoL.push(pako.deflate(payload.cCanData.data))
      state.mCan_undoL.push(pako.deflate(payload.mCanData.data))
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
    storeMCan(state, payload) {
      state.mCan_dic[payload.num] = pako.deflate(payload.imgData.data)
    },
    storeCCan(state, payload) {
      state.cCan_dic[payload.num] = pako.deflate(payload.imgData.data)
    },
    storeCWater(state, payload) {
      state.cWater_dic[payload.num] = pako.deflate(payload.imgData.data)
    },
  },
})
