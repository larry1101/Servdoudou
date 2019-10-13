<template>
  <div>
    <mu-appbar style="width: 100%;" color="primary" class="topFixed">

      <mu-button icon v-if="!adm">
        <mu-icon value="mood" :color="admbc"></mu-icon>
      </mu-button>
      Idioum
      <mu-button icon @click="tryAdm" v-if="!adm">
        <mu-icon value="mood" :color="admbc"></mu-icon>
      </mu-button>

      <mu-button flat slot="left" @click="onSearch">
        <mu-icon value="search"></mu-icon>
      </mu-button>
      <mu-menu slot="left" v-if="adm" :open.sync="manmenuopen">
        <mu-button flat>
          <mu-icon value="build"></mu-icon>
        </mu-button>
        <mu-list slot="content">
          <mu-list-item button @click="dwni" ripple-color="green">
            <mu-list-item-content>
              <mu-list-item-title>下载备份json</mu-list-item-title>
            </mu-list-item-content>
          </mu-list-item>
          <mu-list-item button @click="addi" ripple-color="yellow">
            <mu-list-item-content>
              <mu-list-item-title>追加数据库</mu-list-item-title>
            </mu-list-item-content>
          </mu-list-item>
          <mu-list-item button @click="mrgi" ripple-color="blue">
            <mu-list-item-content>
              <mu-list-item-title>合并数据库</mu-list-item-title>
            </mu-list-item-content>
          </mu-list-item>
          <mu-list-item button @click="clri" ripple-color="red">
            <mu-list-item-content>
              <mu-list-item-title>覆盖数据库</mu-list-item-title>
            </mu-list-item-content>
          </mu-list-item>
          <mu-list-item button @click="server_ipp='http://127.0.0.1:8000/';manmenuopen=false" ripple-color="red">
            <mu-list-item-content>
              <mu-list-item-title style="color: #f00;">npm building @ localhost:8080</mu-list-item-title>
            </mu-list-item-content>
          </mu-list-item>
        </mu-list>
      </mu-menu>
      <mu-button flat slot="right" @click="refreshNst">
        <mu-icon value="refresh"></mu-icon>
      </mu-button>
      <mu-button flat slot="right" @click="showadder" v-if="adm">
        <mu-icon :value="add_ic"></mu-icon>
      </mu-button>
    </mu-appbar>

    <mu-snackbar position="top" :color="snc.color" :open.sync="snc.open">
      <mu-icon left :value="snc.icon"></mu-icon>
      {{snc.msg}}
      <mu-button icon slot="action" color="#fff" @click="snc.open = false">
        <mu-icon value="cancel"></mu-icon>
      </mu-button>
      <mu-button slot="action" color="warning" @click="fix_in_57888" v-if="snc.show_fix">
        尝试修复！
      </mu-button>
    </mu-snackbar>

    <div class="contou" :style="contoup" v-resize="onmResize">
      <mu-container ref="idolist" class="contou-cont">
        <mu-load-more @refresh="refresh" :refreshing="refreshing" :loading="loading" @load="load"
                      :loaded-all="loaded_all">
          <mu-list textline="three-line" class="align-left" @change="onitemclk">
            <template v-for="item in list_items">
              <mu-list-item button :value="item">
                <mu-list-item-content>
                  <mu-list-item-title class="li-ltem-t">
                    <mu-flex class="word-title" justify-content="end">
                      <mu-flex fill>
                        <div>{{item.fields.word}}</div>
                      </mu-flex>
                      <mu-flex class="flex-demo" justify-content="center" style="visibility: hidden;">
                        <span slot="right">{{item.pk}}</span>
                      </mu-flex>
                    </mu-flex>
                  </mu-list-item-title>
                  <mu-list-item-sub-title class="li-ltem-sub-t">
                    {{item.fields.meaning}}
                  </mu-list-item-sub-title>
                </mu-list-item-content>
              </mu-list-item>
              <mu-divider/>
            </template>
          </mu-list>
        </mu-load-more>
      </mu-container>
    </div>

    <mu-dialog :open.sync="moauth" overlay-color="red">
      <mu-flex slot="title" align-items="center">
        <mu-icon :value="oauthico" color="error"></mu-icon>
        <span>{{oauthstr}}</span>
      </mu-flex>
      <div v-if="!oauthed">
        <div>
          <mu-flex justify-content="center">
            <mu-button icon @click="oauths+='0'">你</mu-button>
            <mu-button icon @click="oauths+='2'">权</mu-button>
            <mu-button icon @click="oauths+='3'">限</mu-button>
            <mu-button icon @click="oauths+='4'">呢</mu-button>
            <mu-button icon @click="oauths+='9'">?</mu-button>
          </mu-flex>
          <mu-flex justify-content="center">
            <mu-button icon @click="oauths+='5'">我</mu-button>
            <mu-button icon @click="oauths+='6'">没</mu-button>
            <mu-button icon @click="oauths+='7'">有</mu-button>
            <mu-button icon @click="oauths+='8'">啊</mu-button>
            <mu-button icon @click="startOauth">！</mu-button>
          </mu-flex>
        </div>
      </div>
      <div v-if="oauthed">
        <div>
          <el-upload
            :action="upladdr"
            :before-upload="beforeUpl"
            :limit="1"
            :on-error="uplErr"
            :on-success="uplSuc"
            accept="application/json"
            :headers="{'X-CSRFtoken': this.getCookie('csrftoken')}"
            :data="{'act': this.iact}"
          >
            <mu-button color="primary" full-width>点击上传</mu-button>
            <div slot="tip" class="el-upload__tip">请选择备份的 idioums.json 文件</div>
          </el-upload>
        </div>
      </div>
      <mu-button slot="actions" flat color="primary" @click="closeOauthDialog">关闭</mu-button>
    </mu-dialog>

    <mu-dialog :title="dlgW" width="90%" :open.sync="openDet">
      <div>
        <mu-flex justify-content="between" align-items="center">
          <div>
            <mu-button flat @click="search_baidu(dlgW)" color="primary" round>百度一下</mu-button>
            <mu-button flat @click="search_baidu_baike(dlgW)" color="primary" round>百度百科</mu-button>
          </div>
          <div>
            <span>{{dlgPos}}</span>
          </div>
          <div v-if="adm">
            <mu-button icon color="error" @click="clr_dlgm" :disabled="cannot_edit">
              <mu-icon right value="clear"></mu-icon>
            </mu-button>
            <mu-button icon color="error" @click="del_ido">
              <mu-icon right value="delete"></mu-icon>
            </mu-button>
            <mu-button icon color="primary" @click="edit_ido">
              <mu-icon right value="edit"></mu-icon>
            </mu-button>
          </div>
        </mu-flex>
        <div>
          <mu-text-field
            ref="valdm"
            v-model="dlgM" label="Ctrl + ← 提交"
            full-width label-float multi-line
            :rows="4" :rows-max="10" :max-length="250"
            :disabled="cannot_edit"
            @keydown.ctrl.left="comfrim_edit"
          ></mu-text-field>
        </div>
      </div>
      <mu-button slot="actions" flat color="warning" @click="addPri">
        <mu-icon value="sentiment_very_dissatisfied"></mu-icon>
        多看
      </mu-button>
      <mu-button slot="actions" flat color="success" @click="minusPri">
        <mu-icon value="sentiment_very_satisfied"></mu-icon>
        会了
      </mu-button>
      <mu-button slot="actions" flat color="primary" @click="closeDetailDialog">
        好
      </mu-button>
    </mu-dialog>

    <mu-dialog title="Delete" :open.sync="redel">
      <mu-flex justify-content="center">
        <span style="color: red">Really?</span>
      </mu-flex>
      <mu-flex justify-content="between" align-items="center">
        <mu-button flat color="error" @click="comfrim_del">Delete</mu-button>
        <mu-button flat color="primary" @click="not_del">Back</mu-button>
      </mu-flex>
    </mu-dialog>

    <mu-dialog width="100%" transition="slide-bottom" fullscreen :open.sync="openSearch">
      <mu-appbar color="primary" title="Search">
        <mu-button slot="left" icon @click="closeSearchDialog">
          <mu-icon value="arrow_back"></mu-icon>
        </mu-button>
      </mu-appbar>
      <div style="padding: 24px;">
        <mu-flex justify-content="between" align-items="center">
          <mu-text-field
            ref="svi"
            v-model="val_si"
            label="idiom"
            full-width label-float :max-length="15"
            @keypress.enter="searchido"
            @keydown.ctrl.left="val_si=''"
          ></mu-text-field>
          <mu-button icon @click="searchido">
            <mu-icon value="search"></mu-icon>
          </mu-button>
        </mu-flex>
        <mu-flex justify-content="between">
          {{val_sis}}
        </mu-flex>
        <mu-flex justify-content="between">
          {{val_sm}}
        </mu-flex>
        <mu-flex justify-content="center" v-if="show_search_add">
          <mu-button full-width color="success" @click="quick_add_search">添加这个词</mu-button>
        </mu-flex>
      </div>
    </mu-dialog>

    <mu-slide-bottom-transition>
      <div class="bottomFixed" v-if="show_add">
        <mu-paper round class="add-paper" :z-depth="4">
          <mu-container>
            <mu-flex justify-content="end">
              <mu-button flat @click="showadder">
                <mu-icon value="arrow_drop_down"></mu-icon>
                关闭
              </mu-button>
            </mu-flex>
            <mu-flex justify-content="between" align-items="center">
              <mu-text-field
                ref="validi"
                v-model="val_i"
                label="idiom Enter 切换；Ctrl+Enter提交、+↑百度、+↓百科、+Del清空"
                full-width label-float :max-length="15"
                @keypress.enter="vali_chg"
                @keydown.ctrl.enter="addido"
                @keydown.ctrl.right="search_baidu(val_i)"
                @keydown.ctrl.down="search_baidu_baike(val_i)"
                @keydown.ctrl.delete="val_i='',val_m=''"
              ></mu-text-field>
              <mu-button icon @click="val_i=''" color="error">
                <mu-icon value="clear"></mu-icon>
              </mu-button>
            </mu-flex>
            <mu-flex justify-content="between" align-items="center">
              <mu-text-field
                ref="valm"
                v-model="val_m" label="meaning Ctrl Enter 提交"
                multi-line
                full-width label-float :rows="4" :max-length="250"
                @keydown.ctrl.enter="valm_ok"
                @focus="onvalmfocus"
                @keydown.ctrl.delete="val_i='',val_m=''"
              ></mu-text-field>
              <mu-button icon @click="val_m=''" color="error">
                <mu-icon value="clear"></mu-icon>
              </mu-button>
            </mu-flex>
            <mu-row>
              <mu-button full-width color="success" @click="addido">
                Add
              </mu-button>
            </mu-row>
          </mu-container>
        </mu-paper>
      </div>
    </mu-slide-bottom-transition>

  </div>
</template>

<script>
  export default {
    name: "indx",
    data() {
      return {
        server_ipp: 'http://127.0.0.1:8000/',

        winH: 0,

        refreshing: false,
        loading: false,
        list_items: [],
        loaded_all: false,

        val_i: '',
        val_m: '',

        show_add: false,
        // show_add: true,
        contmb: 0,
        add_ic: 'add',

        openDet: false,
        dlgW: 'idiom',
        dlgM: 'meaning',
        dlgid: 0,
        dlgPos: 0,

        redel: false,

        cannot_edit: true,

        snc: {
          color: 'info',
          icon: 'info',
          msg: '-',
          timeout: 2000,
          open: false,
          show_fix: false,
        },

        openSearch: false,
        val_si: '',
        val_sis: '',
        val_sm: '',
        show_search_add: false,

        adi: 0,
        adm: false,
        admbc: 'blue100',

        manmenuopen: false,
        iact: '',
        oauths: '',
        oauthed: false,
        upladdr: '',
        oauthstr: '权限需要',
        oauthico: 'warning',
        moauth: false,
        csrftoken: '',
      }
    },

    computed: {
      contoup: function () {
        return {
          paddingBottom: this.contmb + 'px',
          height: this.winH + 'px',
        }
      }
    },

    methods: {

      refreshNst() {
        this.refresh()
        this.mscrollTop()
      },

      mscrollTop() {
        this.$refs.idolist.scrollTop = 0;
      },

      refresh() {
        this.refreshing = true
        this.loaded_all = false
        this.$axios.get(this.server_ipp + 'api/show_idioms')
          .then((res) => {
            this.list_items = []
            // console.log(res)
            for (let idoi in res.data.list) {
              // console.log(res.data.list[idoi])
              this.list_items.push(res.data.list[idoi])
            }
            // console.log(this.list_items)
            this.refreshing = false;
            if (res.data.list.length < 10) {
              this.loaded_all = true
            }
            console.log('Idioums: ' + res.data.list.length)
          }).catch((error) => {
          console.log('Error:', error)
          this.refreshing = false;
        })
      },

      load() {
        // this.loading = true;
        // this.$axios.get('http://127.0.0.1:8000/api/show_idioms', {
        //   params: {
        //     prev: this.list_items.length,
        //     count: 10
        //   }
        // }).then((res) => {
        //   for (let idoi in res.data.list) {
        //     this.list_items.push(res.data.list[idoi])
        //   }
        //   this.loading = false;
        //   console.log(res.data.list.length)
        //   if (res.data.list.length < 10) {
        //     this.loaded_all = true
        //   }
        // }).catch((error) => {
        //   console.log('Error:', error)
        //   this.loading = false;
        // })
      },

      showadder() {
        this.show_add = !this.show_add
        if (this.show_add) {
          this.contmb = 268
          this.add_ic = 'remove'
        } else {
          this.contmb = 0
          this.add_ic = 'add'
        }
        setTimeout(() => {
          if (this.show_add) {
            this.$refs.validi.focus()
          }
        }, 400)
      },

      vali_chg(e) {
        // console.log(this.$refs.validi.value)
        if (this.$refs.validi.value === '')
          return
        this.$refs.valm.focus()
      },

      onvalmfocus() {
        if (this.$refs.validi.value === '')
          return
        this.$axios.get(this.server_ipp + 'api/get_idiom', {
          params: {
            word: this.val_i,
          }
        }).then((res) => {
          if (res.data.error_num === 0) {
            this.val_m = res.data.idiom.fields.meaning
          }
        }).catch((error) => {
          console.log('Try to get idiom error:', error)
        })
      },

      valm_ok(e) {
        this.addido()
      },

      addido() {
        if (this.val_i === '') {
          return
        }
        this.$axios.post(
          this.server_ipp + 'api/add_idiom',
          this.$qs.stringify({
            word: this.val_i,
            meaning: this.val_m,
          }),
          {
            headers: {
              'X-CSRFtoken': this.getCookie('csrftoken'),
              'Content-Type': 'application/x-www-form-urlencoded',
            }
          }).then((res) => {
          // console.log(res)
          if (res.data.error_num === 0)
            this.snc_msg('check_circle', 'success', '添加成功')
          else if (res.data.error_num === 1)
            this.snc_msg('info', 'warning', '已存在，没写意思不会更新')
          else if (res.data.error_num === 2)
            this.snc_msg('info', 'warning', '已存在，意思一样不会更新')
          else if (res.data.error_num === 3)
            this.snc_msg('info', 'info', '已存在，已更新')
          this.refresh()
          this.val_i = ''
          this.val_m = ''
          // this.$axios.get('http://127.0.0.1:8000/api/get_last_idiom')
          //   .then((res) => {
          //     // console.log(res.data)
          //     // console.log(res.data.idiom)
          //     // this.list_items.push(res.data.idiom)
          //   }).catch((error) => {
          //   console.log('Error:', error)
          //   this.loading = false;
          // })
          this.$refs.validi.focus()
          // console.log(this.$refs.idolist)
          // console.log(this.$refs.idolist.scrollTop)
          // console.log(this.$refs.idolist.scrollHeight)
          setTimeout(() => {
            this.$refs.idolist.scrollTop = this.$refs.idolist.scrollHeight;
          }, 150)
        }).catch((error) => {
          console.log('Error:', error)
          this.snc_msg('warning', 'error', error)
        })
      },

      openDetailDialog() {

        this.openDet = true;
        if (this.dlgM === '') {
          this.cannot_edit = false
          setTimeout(() => {
            if (!this.cannot_edit) {
              this.$refs.valdm.focus()
            }
          }, 250)
        } else {
          this.cannot_edit = true
        }
      },

      closeDetailDialog() {
        if (!this.cannot_edit) {
          this.comfrim_edit()
        }
        this.openDet = false;
      },

      addPri() {
        this.$axios.post(this.server_ipp + 'api/mov_idiom',
          {
            iid: this.dlgid,
            word: this.dlgW,
            meaning: this.dlgM,
            addp: true,
          }, {
            headers: {'X-CSRFtoken': this.getCookie('csrftoken'),}
          }).then((res) => {
          // console.log(res)
          if (res.data.error_num === 0)
            this.snc_msg('check_circle', 'success', '已更新')
          else if (res.data.error_num === 1)
            this.snc_msg('info', 'error', '无记录')
          else if (res.data.error_num === 2)
            this.snc_msg('info', 'warning', '不会更新')
          else if (res.data.error_num === 3)
            this.snc_msg('info', 'info', '意思没变')
          this.openDet = false;
          this.refresh()
        }).catch((error) => {
          console.log('Error:', error)
          this.snc_msg('warning', 'error', error)
        })
      },

      minusPri() {
        this.$axios.post(this.server_ipp + 'api/mov_idiom',
          {
            iid: this.dlgid,
            word: this.dlgW,
            meaning: this.dlgM,
            addp: false,
          }, {
            headers: {'X-CSRFtoken': this.getCookie('csrftoken'),}
          }).then((res) => {
          // console.log(res)
          if (res.data.error_num === 0)
            this.snc_msg('check_circle', 'success', '已更新')
          else if (res.data.error_num === 1)
            this.snc_msg('info', 'error', '无记录')
          else if (res.data.error_num === 2)
            this.snc_msg('info', 'warning', '不会更新')
          else if (res.data.error_num === 3)
            this.snc_msg('info', 'info', '意思没变')
          this.openDet = false;
          this.refresh()
        }).catch((error) => {
          console.log('Error:', error)
          this.snc_msg('warning', 'error', error)
        })
      },

      onitemclk(ido) {
        this.dlgW = ido.fields.word
        this.dlgM = ido.fields.meaning
        this.dlgid = ido.pk
        this.dlgPos = ido.fields.pos
        this.openDetailDialog()
      },

      del_ido() {
        this.redel = true
      },

      comfrim_del() {
        this.$axios.post(this.server_ipp + 'api/del_idiom',
          this.$qs.stringify({
            iid: this.dlgid,
            word: this.dlgW,
            meaning: this.dlgM,
          }),
          {
            headers: {
              'X-CSRFtoken': this.getCookie('csrftoken'),
              'Content-Type': 'application/x-www-form-urlencoded',
            }
          }).then((res) => {
          this.openDet = false;
          this.redel = false
          this.snc_msg('priority_high', 'info', 'Idiom deleted')
          this.refresh()
        }).catch((error) => {
          console.log('Error:', error)
          this.snc_msg('warning', 'error', error)
          this.redel = false
        })
      },

      not_del() {
        this.redel = false
      },

      edit_ido() {
        this.cannot_edit = !this.cannot_edit
        setTimeout(() => {
          if (!this.cannot_edit) {
            this.$refs.valdm.focus()
          }
        }, 250)
      },

      clr_dlgm() {
        this.dlgM = ''
        this.$refs.valdm.focus()
      },

      comfrim_edit() {
        this.$axios.post(this.server_ipp + 'api/edi_idiom',
          this.$qs.stringify({
            iid: this.dlgid,
            word: this.dlgW,
            meaning: this.dlgM,
          }),
          {
            headers: {
              'X-CSRFtoken': this.getCookie('csrftoken'),
              'Content-Type': 'application/x-www-form-urlencoded',
            }
          }).then((res) => {
          // console.log(res)
          if (res.data.error_num === 0)
            this.snc_msg('check_circle', 'success', '已更新')
          else if (res.data.error_num === 1)
            this.snc_msg('info', 'error', '无记录')
          else if (res.data.error_num === 2)
            this.snc_msg('info', 'warning', '不会更新')
          else if (res.data.error_num === 3)
            this.snc_msg('info', 'info', '意思没变')
          this.openDet = false;
          this.refresh()
        }).catch((error) => {
          console.log('Error:', error)
          this.snc_msg('warning', 'error', error)
        })
      },

      snc_msg(icon = 'info', color = 'info', msg = '', timeout = 2000) {
        this.snc.icon = icon
        this.snc.color = color
        this.snc.msg = msg
        this.snc.timeout = timeout
        this.snc.open = true

        if (color === 'error') {
          this.snc.show_fix = true
          this.snc.timeout = 3999
        } else {
          this.snc.show_fix = false
        }

        setTimeout(() => {
          this.snc.open = false
        }, this.snc.timeout)
      },

      fix_in_57888() {
        // 如果index.html由nginx提供，那么就没有csrftoken，这样就没法post
        // 直接进一次uwsgi提供的页面后就有csrf token了……
        // 同时也能进后台了……
        // 超级迷惑……
        // console.log(window.location.hostname)
        window.open('http://'+window.location.hostname+':57888/sitepanel')
      },

      onSearch() {
        this.openSearch = true
        setTimeout(() => {
          this.$refs.svi.focus()
        }, 500)
      },

      closeSearchDialog() {
        this.openSearch = false
      },

      searchido() {
        this.$axios.get(this.server_ipp + 'api/get_idiom', {
          params: {
            word: this.val_si,
          }
        }).then((res) => {
          if (res.data.error_num === 0) {
            this.val_si = ''
            this.val_sis = res.data.idiom.fields.word
            this.val_sm = res.data.idiom.fields.meaning
            this.show_search_add = false
          } else {
            // this.val_si=''
            this.val_sis = '查找失败'
            this.val_sm = ''
            this.show_search_add = true
          }
        }).catch((error) => {
          console.log('Try to get idiom error:', error)
        })
        this.$refs.svi.focus()
      },

      quick_add_search() {
        this.$axios.post(
          this.server_ipp + 'api/add_idiom',
          this.$qs.stringify({
            word: this.val_si,
            meaning: '',
          }),
          {
            headers: {
              'X-CSRFtoken': this.getCookie('csrftoken'),
              'Content-Type': 'application/x-www-form-urlencoded',
            }
          }).then((res) => {
          if (res.data.error_num === 0)
            this.snc_msg('check_circle', 'success', '添加成功')
          else if (res.data.error_num === 1)
            this.snc_msg('info', 'warning', '已存在，没写意思不会更新')
          else if (res.data.error_num === 2)
            this.snc_msg('info', 'warning', '已存在，意思一样不会更新')
          else if (res.data.error_num === 3)
            this.snc_msg('info', 'info', '已存在，已更新')
          this.val_si = ''
          this.show_search_add = false
          this.refresh()
        }).catch((error) => {
          console.log('Error:', error)
          this.snc_msg('warning', 'error', error)
        })
      },

      onmResize() {
        this.winH = window.innerHeight
      },

      tryAdm() {
        if (this.adi <= 1) {
          this.adi++
        } else if (this.adi <= 2) {
          this.adi++
          this.admbc = 'deepPurple300'
        } else if (this.adi <= 3) {
          this.adi++
          this.admbc = 'pink50'
        } else {
          this.admbc = 'lightGreen50'
          this.adm = true
        }
      },

      dwni() {
        window.open(this.server_ipp + 'api/download_ido')
        this.manmenuopen = false
      },

      mrgi() {
        this.oauths = ''
        this.oauthed = false
        this.moauth = true
        this.oauthstr = '权限需要'
        this.oauthico = 'warning'
        this.manmenuopen = false
        this.iact = 'mrg'
      },

      clri() {
        this.oauths = ''
        this.oauthed = false
        this.moauth = true
        this.oauthstr = '权限需要'
        this.oauthico = 'warning'
        this.manmenuopen = false
        this.iact = 'clr'
      },

      addi() {
        this.oauths = ''
        this.oauthed = false
        this.moauth = true
        this.oauthstr = '权限需要'
        this.oauthico = 'warning'
        this.manmenuopen = false
        this.iact = 'add'
      },

      startOauth() {
        this.$axios.get(this.server_ipp + 'api/get_upl', {
          params: {
            pid: this.oauths,
          }
        }).then((res) => {
          // console.log(res)
          if (res.data.upl) {
            this.upladdr = this.server_ipp + res.data.addr
            this.oauthed = true
            this.oauthstr = '上传文件'
            this.oauthico = 'info'
            this.csrftoken = res.data.csrft
            // this.moauth = false
            // show upl dlg
          }
        }).catch((error) => {
          console.log('Error:', error)
        })
        this.oauths = ''
      },

      beforeUpl(file) {
        // console.log(file, file.type)
        if (file.type !== 'application/json') {
          this.$toast.error({message: '需要json文件', position: 'top'});
          return false;
        }
        return true;
      },

      uplErr(err, file, fileList) {
        this.$toast.error({message: '上传失败了' + err, position: 'top'});
        // console.log(err, file, fileList)
      },

      uplSuc(response, file, fileList) {
        // console.log(response, file, fileList)
        if (response.error_num !== 0) {
          this.$toast.error({message: response.msg, position: 'top'});
          fileList.pop()
          return
        }
        let msg = '上传成功'
        if (response.add !== 0) {
          msg += '，插入' + response.add + '条'
        }
        if (response.ins !== 0) {
          msg += '，更新' + response.ins + '条'
        }
        this.$toast.success({message: msg, position: 'top'});
        fileList.pop()
        this.oauths = ''
        this.oauthed = false
        this.moauth = false
        this.oauthstr = '权限需要'
        this.oauthico = 'warning'
        this.iact = ''
        this.refresh()
        setTimeout(() => {
          this.$refs.idolist.scrollTop = this.$refs.idolist.scrollHeight;
        }, 150)
      },

      closeOauthDialog() {
        this.moauth = false
      },

      search_baidu(val) {
        window.open('https://www.baidu.com/s?wd=' + val)
      },

      search_baidu_baike(val) {
        window.open('https://baike.baidu.com/item/' + val)
      },

      getCookie(name) {
        var value = '; ' + document.cookie
        var parts = value.split('; ' + name + '=')
        if (parts.length === 2) return parts.pop().split(';').shift()
      },

    },

    mounted() {
      this.winH = window.innerHeight
      this.server_ipp = window.location.origin + '/'
      this.refresh()
    }
  }
</script>

<style scoped>
  .contou {
    padding-top: 64px;
    width: 100%;
    max-width: 100%;
    display: flex;
    flex-direction: column;
  }

  .contou-cont {
    flex: 1;
    overflow: auto;
    -webkit-overflow-scrolling: touch;
  }

  .bottomFixed {
    position: fixed;
    width: 100%;
    left: 0;
    bottom: 0;
    z-index: 1000;
  }

  .topFixed {
    position: fixed;
    width: 100%;
    left: 0;
    top: 0;
    z-index: 1000;
  }

  .align-left {
    text-align: left;
  }

  .li-ltem-t {
    /*margin: 3px;*/
    padding: 0px 2px 0px;
    width: 100%;
  }

  .li-ltem-sub-t {
    padding: 2px 2em;
    width: 100%;
  }

  .add-paper {
    padding: 2px 4px 6px;
  }

  .word-title {
  }
</style>
