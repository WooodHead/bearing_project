/**
 * Created by zhanghe on 16-1-31.
 */

/* 轮播大图延时加载 */
function lazyContainer (searchNode) {
    $(searchNode).find('.active').find('img.lazy').each(function () {
        var imgSrc = $(this).attr('data-src')
        if (imgSrc) {
            $(this).attr('src', imgSrc)
            $(this).attr('data-src', '')
        }
    })
}

$('#myCarousel').bind('slid.bs.carousel', function () {
    lazyContainer(this)
})

lazyContainer('#myCarousel')

/* 生成工具提示 */
$('[rel="tooltip"]').tooltip()

/* 附加导航 */
$(function () {
    // 滚动页面侧边悬浮动态导航宽度控制
    $(window).resize(function () {
        $('#affix_nav_ul').width($('#affix_nav_ul').parent().width())
        //console.log($('.container').width());
        // 如果屏幕宽度小于940px 隐藏侧边导航
        if ($('.container').width() <= 940) {
            $('#affix_nav_ul').hide()
        } else {
            $('#affix_nav_ul').show()
        }
    })
    $(window).resize()
})

/* 按钮加载状态 */
// html button 标签其中 autocomplete="off" 属性是针对FF浏览器在页面加载之后，禁用状态不会自动解除用的。
$(function () {
    $('.btn-load').click(function () {
        $(this).button('loading').delay(1000).queue(function () {
            $(this).button('reset').dequeue()
        })
    })
})

/* 返回顶部 */
$('#top-link').click(function () {
    $('html,body').animate({scrollTop: 0}, 'slow')
    return false
})
if (($(window).height() + 100) < $(document).height()) {
    $('#top-link-block').removeClass('hidden').affix({
        // how far to scroll down before link "slides" into view
        offset: {top: 100}
    })
}

/* 侧滑插件 */
/*
var slideout = new Slideout({
    'panel': document.getElementById('panel'),
    'menu': document.getElementById('menu'),
    'padding': 256,
    'tolerance': 70
});
 */

/**
 * Vertically center Bootstrap 3 modals so they aren't always stuck at the top
 */
$(function () {
    function reposition () {
        var modal = $(this),
            dialog = modal.find('.modal-dialog')
        modal.css('display', 'block')

        // Dividing by two centers the modal exactly, but dividing by three
        // or four works better for larger screens.
        dialog.css('margin-top', Math.max(0, ($(window).height() - dialog.height()) / 2))
    }

    // Reposition when a modal is shown
    $('.modal').on('show.bs.modal', reposition)
    // Reposition when the window is resized
    $(window).on('resize', function () {
        $('.modal:visible').each(reposition)
    })
})

/**
 * 闪现消息
 * 通知类型自动关闭（alert-success,alert-warning,alert-danger）
 * 消息类型保持不动（alert-info）
 */
$('.alert-success,.alert-warning,.alert-danger').fadeTo(3500, 0.8).slideUp(500, function () {
    $(this).slideUp(500)
})

/*按钮虚框移除*/
$('button').on('click', function () {
    $(this).blur();
})

/*数据行超链接阻止冒泡*/
$(function() {
    $("tr.item>td a").click(function(event) {
        event.stopPropagation();
    });
});

$(function () {
    var prev_page = $('.prev')
    var next_page = $('.next')
    $('body').keydown(function (event) {
        if (event.keyCode === 37 && prev_page !== undefined) prev_page.click();
        if (event.keyCode === 39 && next_page !== undefined) next_page.click();
    })
})
