App({
  onLaunch: function () {
    var that = this;
    wx.login({
      success: res => {
        wx.request({
          url: that.globalData.wx_url_1 + res.code + that.globalData.wx_url_2, 
          success: res => {
            that.globalData.openid = res.data.openid;
          }
        })
      }
    });
    //调用API从本地缓存中获取数据
    var logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)
  },
  //第一种状态的底部
  editTabBar: function () {
    var _curPageArr = getCurrentPages();
    var _curPage = _curPageArr[_curPageArr.length - 1];
    var _pagePath = _curPage.__route__;
    if (_pagePath.indexOf('/') != 0) {
      _pagePath = '/' + _pagePath;
    }
    var tabBar = this.globalData.tabBar;
    for (var i = 0; i < tabBar.list.length; i++) {
      tabBar.list[i].active = false;
      if (tabBar.list[i].pagePath == _pagePath) {
        tabBar.list[i].active = true;//根据页面地址设置当前页面状态  
      }
    }
    _curPage.setData({
      tabBar: tabBar
    });
  },
  getUserInfo: function (cb) {
    var that = this
    if (this.globalData.userInfo) {
      typeof cb == "function" && cb(this.globalData.userInfo)
    } else {
      //调用登录接口
      wx.login({
        success: function () {
          wx.getUserInfo({
            success: function (res) {
              that.globalData.userInfo = res.userInfo
              typeof cb == "function" && cb(that.globalData.userInfo)
            }
          })
        }
      })
    }
  },
  globalData: {
    openid: 0,
    wx_url_1: 'https://api.weixin.qq.com/sns/jscode2session?appid=	wx2071a5e1300f1120&secret=4a02d51cf338be5a40f00bf55689226a&js_code=',
    wx_url_2: '&grant_type=authorization_code',
    inputvalues: null,
    pointValues: '',
    feeValues: '',
    userInfo: null,
    tabBar: {
      "color": "#8a8a8a",
      "selectedColor": "#2c2c2c",
      "backgroundColor": "#ffffff",
      "list": [
        {
          "pagePath": "/pages/index/index",
          "text": "REGRESSION",
          "iconPath": "/img/regression_gr.png",
          "selectedIconPath": "/img/regression_or.png",
          "clas": "menu-item3",
          "selectedColor": "#000000",
          active: true
        },
        {
          "pagePath": "/pages/history/history",
          "text": "HISTORY",
          "iconPath": "/img/history_gr.png",
          "selectedIconPath": "/img/history_or.png",
          "selectedColor": "#000000",
          "clas": "menu-item3",
          active: true
        }
      ],
      "position": "bottom"
    },
  }
})