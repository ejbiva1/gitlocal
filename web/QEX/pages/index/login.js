Page({ 
  data: {
    canIUse: wx.canIUse('button.open-type.getUserInfo')
  },
  onLoad: function () {
    var that = this;
    wx.getSetting({
      success: function (res) {
        if (res.authSetting['scope.userInfo']) {    
          wx.getUserInfo({
            success: function (res) {
              that.queryUsreInfo(); 
              wx.redirectTo({
                url:'index'
              })
            }
          });
        }
      }
    })
  },
  bindGetUserInfo: function (e) {
    if (e.detail.userInfo) {
      var that = this;
      wx.redirectTo({
        url:'index'
      })
    } else {
      wx.showModal({
        title:'警告',
        content:'您点击了拒绝授权，将无法进入小程序，请授权之后再进入!',
        showCancel:false,
        confirmText:'返回授权',
        success:function(res){
          if (res.confirm) {
            console.log('用户点击了“返回授权”')
          }
        }
      })
    }
  },
})