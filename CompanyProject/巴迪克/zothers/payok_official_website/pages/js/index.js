// 页面初始化
$(document).ready(function() {
     // 检查是否为移动设备
     if($(window).width() > 768) {
        initScrollAnimations();
    } else {
        // 移动端滑动处理
        const sliderContainer = $('.events-slider-container');
        const slider = $('.events-slider');
        const cards = $('.event-card');
        
        // 移动端限制为8个卡片
        if (cards.length > 8) {
            cards.slice(8).remove();
        }
        
        let startX = 0;
        let currentX = 0;
        let initialTranslate = 0;
        let isUserInteracting = false;
        
        // 清除可能存在的旧计时器
        if (interval) {
            clearInterval(interval);
            interval = null;
        }
        
        // 简化触摸事件处理
        sliderContainer[0].addEventListener('touchstart', function(e) {
            isUserInteracting = true;
            startX = e.touches[0].clientX;
            
            // 获取当前位置
            const transform = slider.css('transform');
            const matrix = transform.match(/matrix\((.+)\)/);
            if (matrix) {
                initialTranslate = parseInt(matrix[1].split(', ')[4]) || 0;
                autoScrollPosition = initialTranslate; // 同步自动滚动位置
            } else {
                initialTranslate = 0;
                autoScrollPosition = 0;
            }
            
            // 停止动画
            slider.css('transition', 'none');
            
            // 暂停自动滚动
            if (interval) {
                clearInterval(interval);
                interval = null;
            }
            
            // 取消动画帧，确保自动滚动完全停止
            if (animationFrameId) {
                cancelAnimationFrame(animationFrameId);
                animationFrameId = null;
            }
        }, {passive: false});

        sliderContainer[0].addEventListener('touchmove', function(e) {
            if (!isUserInteracting) return;
            
            currentX = e.touches[0].clientX;
            const diff = currentX - startX;
            
            // 计算新位置
            const containerWidth = sliderContainer.width();
            const sliderWidth = slider[0].scrollWidth;
            const maxScrollLeft = containerWidth - sliderWidth;
            
            let newTranslate = initialTranslate + diff;
            
            // 边界检查
            if (newTranslate > 0) {
                newTranslate = 0;
            } else if (newTranslate < maxScrollLeft) {
                newTranslate = maxScrollLeft;
            }
            
            // 应用转换
            slider.css('transform', `translateX(${newTranslate}px)`);
        }, {passive: false});

        sliderContainer[0].addEventListener('touchend', function() {
            // 添加平滑过渡
            slider.css('transition', 'transform 0.3s ease');
            isUserInteracting = false;
            
            // 获取最终位置
            const transform = slider.css('transform');
            const matrix = transform.match(/matrix\((.+)\)/);
            if (matrix) {
                const finalPos = parseInt(matrix[1].split(', ')[4]) || 0;
                autoScrollPosition = finalPos; // 更新自动滚动位置
                
                // 取消可能存在的动画帧
                if (animationFrameId) {
                    cancelAnimationFrame(animationFrameId);
                    animationFrameId = null;
                }
                
                // 检查最后一个卡片是否已进入视图380px
                const lastCard = $('.event-card:last-child');
                const containerWidth = sliderContainer.width();
                const lastCardLeft = lastCard.position().left;
                const stopThreshold = containerWidth - 380;
                
                // 延迟重启自动滚动，给用户更多控制时间
                setTimeout(() => {
                    // 只有当最后一个卡片尚未进入视图380px时，才重启自动滚动
                    if (lastCardLeft > stopThreshold) {
                        startAutoScroll(true);
                    }
                }, 1500); // 延迟1.5秒重启自动滚动
            }
        }, {passive: false});
        
        // 启动移动端自动滚动
        startAutoScroll(true);
        
        // 添加滑块容器的可见性监测
        const sliderObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    // 滑块进入视图，重新启动自动滚动
                    if (!animationFrameId && autoScrollPosition !== 0) {
                        startAutoScroll(true);
                    }
                } else {
                    // 滑块离开视图，停止自动滚动
                    if (animationFrameId) {
                        cancelAnimationFrame(animationFrameId);
                        animationFrameId = null;
                    }
                }
            });
        }, { threshold: 0.1 });
        
        // 开始观察滑块容器
        sliderObserver.observe(sliderContainer[0]);
    }

    // 首屏动画
    setTimeout(() => {
        initFirstSection();
        initEventSlider();
        
        // 仅在非移动设备上初始化自动滚动
        if($(window).width() > 768) {
            startAutoScroll(false);
        }
    }, 1000);
});

// 全局变量，用于requestAnimationFrame
let animationFrameId = null;
let lastTimestamp = 0;
let scrollSpeed = 0.2; // 降低滚动速度

// 启动自动滚动功能
function startAutoScroll(isMobile) {
    // 如果滑块不在视图中，不启动自动滚动（仅限移动端）
    if (isMobile) {
        const sliderContainer = $('.events-slider-container');
        const rect = sliderContainer[0].getBoundingClientRect();
        const isVisible = (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= window.innerHeight &&
            rect.right <= window.innerWidth
        );
        
        if (!isVisible) {
            return;
        }
    }
    
    if (interval) {
        clearInterval(interval);
        interval = null;
    }
    
    // 取消可能存在的动画帧
    if (animationFrameId) {
        cancelAnimationFrame(animationFrameId);
        animationFrameId = null;
    }
    
    // 移动设备时初始化 autoScrollPosition
    if (isMobile && autoScrollPosition === 0) {
        // 确保初始位置是从0开始
        $('.events-slider').css('transform', 'translateX(0px)');
    }
    
    // 使用requestAnimationFrame实现更平滑的滚动
    if (isMobile) {
        lastTimestamp = performance.now();
        animateScroll();
    } else {
        // PC端保持原有的实现
        interval = setInterval(function() {
            $('.events-slider').css('transform', 'translateX(' + autoScrollPosition + 'px)');
            autoScrollPosition -= 1;
        }, 50);
    }
    
    // 使用requestAnimationFrame实现平滑滚动
    function animateScroll(timestamp) {
        if (!timestamp) {
            timestamp = performance.now();
        }
        
        // 计算时间差，确保在不同刷新率的设备上有一致的滚动速度
        const elapsed = timestamp - lastTimestamp;
        if (elapsed > 0) {
            // 移动设备自动滚动逻辑
            const slider = $('.events-slider');
            const sliderContainer = $('.events-slider-container');
            const lastCard = $('.event-card:last-child');
            
            // 计算容器和最后一个卡片的位置信息
            const containerWidth = sliderContainer.width();
            const lastCardLeft = lastCard.position().left;
            
            // 当最后一个卡片进入屏幕380px时停止滚动
            const stopThreshold = containerWidth - 360;
            
            if (lastCardLeft <= stopThreshold) {
                // 已达到停止条件，不再请求新的动画帧
                return;
            }
            
            // 根据经过的时间调整滚动距离，确保平滑
            const pixelsToScroll = scrollSpeed * (elapsed / 10); // 16ms是60fps的帧间隔
            autoScrollPosition -= pixelsToScroll;
            slider.css('transform', `translateX(${autoScrollPosition}px)`);
            
            lastTimestamp = timestamp;
        }
        
        // 请求下一帧动画
        animationFrameId = requestAnimationFrame(animateScroll);
    }
}

// 首屏动画
function initFirstSection() {
    $('.first-section .bg-left').addClass('active');
    $('.first-section .bg-right').addClass('active');

    const cards = document.querySelectorAll('.stats-card');
        
    function showCards() {
        cards.forEach((card, index) => {
            setTimeout(() => {
                card.classList.add('show');
            }, index * 200); // 每张卡片间隔200ms显示
        });
    }

    // 当第一部分进入视图时触发动画
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                showCards();
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.3
    });

    // 观察stats-container
    const container = document.querySelector('.stats-container');
    if (container) {
        observer.observe(container);
    }
}

let isAutoScrolling = false;
let autoScrollPosition = 0;
let interval;

// 移除 initFullPage 函数，改用滚动观察器
function initScrollAnimations() {
    // 创建观察器实例
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const section = entry.target;
                const sectionId = section.getAttribute('data-section');
                
                switch(sectionId) {
                    case '1':
                        initFirstSection();
                        break;
                    case '2':
                        handleSection2Animations();
                        break;
                    case '3':
                        $('.feature-card, .trusted-partner-card').addClass('animate');
                        break;
                    case '4':
                        $('.video-card, .finrac-card').addClass('animate');
                        break;
                    case '5':
                        handleSection5Animations();
                        break;
                    case '6':
                        handleSection6Animations();
                        break;
                    case '7':
                        $(".custom-navbar").addClass("bgWhite");
                        break;
                }
            }
        });
    }, {
        threshold: 0.3
    });

    // 观察所有section
    document.querySelectorAll('[data-section]').forEach(section => {
        observer.observe(section);
    });
}

// 第二部分动画处理
function handleSection2Animations() {
    // $('#header').addClass('first-header');
    
    // 视频处理
    const video = document.querySelector('.video-background');
    if (video) {
        video.currentTime = 0;
        const playVideo = () => {
            video.play().catch(err => console.log('video play error:', err));
        };
        
        if (video.readyState >= 3) {
            playVideo();
        } else {
            video.addEventListener('canplay', playVideo, { once: true });
        }
    }

    // 数字动画
    const $statNumber = $('.stat-number span');
    $statNumber.each(function() {
        const $this = $(this);
        const target = parseInt($this.attr('data-number'));
        const startValue = parseInt($this.attr('begin'));
        animateNumber($this, target, 3000, startValue);
    });

    // 国旗动画
    const flags = $('.country-tag');
    flags.css({
        'opacity': '0',
        'display': 'block'
    });
    
    flags.each(function(index) {
        setTimeout(() => {
            $(this).css({
                'transition': 'opacity 0.5s ease',
                'opacity': '1'
            });
        }, index * 300);
    });
}

// 第五部分动画处理
function handleSection5Animations() {
    // $('#header').addClass('first-header');
    
    setTimeout(() => {
        $('.fifth-section .events-header').addClass('active');
    }, 100);
    
    setTimeout(() => {
        $('.fifth-section .slider-controls').addClass('active');
    }, 300);
    
    setTimeout(() => {
        $('.fifth-section .events-slider-container').addClass('active');
    }, 500);
}

// 第六部分动画处理
function handleSection6Animations() {
    // $('#header').removeClass('first-header');
    setTimeout(() => {
        $('.slide-from-right').each(function(index) {
            let $this = $(this);
            setTimeout(() => {
                $this.addClass('animate');
            }, index * 200);
        });
    }, 500);
}

// 事件滑块初始化及配置
function initEventSlider() {
    const slider = $('.events-slider');
    const cards = $('.event-card');
    const prevBtn = $('.slider-btn.prev');
    const nextBtn = $('.slider-btn.next');
    const cardWidth = 420;
    const visibleCards = Math.ceil($(window).width() / cardWidth);
    const cloneCount = visibleCards;
    let currentPosition = 0;
    const isMobile = $(window).width() <= 768;

    // 克隆卡片
    function cloneCards() {
        if (isMobile) {
            // 移动端限制为8个卡片并初始化位置
            currentPosition = 0;
            slider.css('transform', 'translateX(0)');
        } else {
            // PC端逻辑修改 - 保持正确顺序
            // 先记录原始卡片
            const originalCards = cards.clone();
            
            // 在前面添加克隆卡片（反向添加，保持正确顺序）
            for(let i = 0; i < cloneCount; i++) {
                for(let j = originalCards.length - 1; j >= 0; j--) {
                    slider.prepend(originalCards.eq(j).clone());
                }
            }
            
            // 在后面添加克隆卡片
            for(let i = 0; i < cloneCount; i++) {
                originalCards.each(function() {
                    slider.append($(this).clone());
                });
            }
            
            // 设置PC端初始位置
            currentPosition = -(cloneCount * cards.length * cardWidth);
            updateSliderPosition(false);
        }
    }

    // 更新滑块位置
    function updateSliderPosition(withTransition = true) {
        slider.css('transition', withTransition ? 'transform 0.5s ease' : 'none');
        slider.css('transform', `translateX(${currentPosition}px)`);
    }

    // 向前滑动处理
    function slidePrev() {
        if (interval) {
            clearInterval(interval);
            interval = null;
        }
        
        if (isMobile) {
            // 移动设备上的逻辑
            const transform = slider.css('transform');
            const matrix = transform.match(/matrix\((.+)\)/);
            if (matrix) {
                currentPosition = parseInt(matrix[1].split(', ')[4]) || 0;
            }
            
            currentPosition += cardWidth;
            if (currentPosition > 0) {
                currentPosition = 0;
            }
        } else {
            // PC设备上的逻辑
            currentPosition += cardWidth;
            if (currentPosition > -(cloneCount * cards.length * cardWidth)) {
                setTimeout(() => {
                    currentPosition -= (cards.length * cardWidth);
                    updateSliderPosition(false);
                }, 500);
            }
        }
        updateSliderPosition();
    }

    // 向后滑动处理
    function slideNext() {
        // 点击清除interval
        if (interval) {
            clearInterval(interval);
            interval = null;
        }
        
        if (isMobile) {
            // 移动设备上的逻辑
            const transform = slider.css('transform');
            const matrix = transform.match(/matrix\((.+)\)/);
            if (matrix) {
                currentPosition = parseInt(matrix[1].split(', ')[4]) || 0;
            }
            
            const containerWidth = $('.events-slider-container').width();
            const sliderWidth = slider.width();
            const maxScrollLeft = containerWidth - sliderWidth;
            
            currentPosition -= cardWidth;
            if (currentPosition < maxScrollLeft) {
                currentPosition = maxScrollLeft;
            }
        } else {
            // PC设备上的逻辑
            currentPosition -= cardWidth;
            if (currentPosition < -((cloneCount + 1) * cards.length * cardWidth)) {
                setTimeout(() => {
                    currentPosition += (cards.length * cardWidth);
                    updateSliderPosition(false);
                }, 500);
            }
        }
        updateSliderPosition();
    }

    // 初始化
    cloneCards();

    prevBtn.click(slidePrev);
    nextBtn.click(slideNext);
    slider.on('transitionend', () => slider.css('transition', 'transform 0.5s ease'));
}

function animateNumber($element, target, duration = 3000, startValue) {
    target = parseInt(target);
    startValue = parseInt(startValue);
    
    const increment = target - startValue;
    
    // calculate steps
    const steps = 60; // 每秒60帧
    const totalSteps = (duration / 1000) * steps;
    const stepIncrement = increment / totalSteps;
    
    // current value
    let currentValue = startValue;
    
    // create animation interval
    const interval = setInterval(() => {
        // increase current value
        currentValue += stepIncrement;
        
        // if already reached or exceeded target value, set to target value and clear interval
        if ((stepIncrement > 0 && currentValue >= target) || 
            (stepIncrement < 0 && currentValue <= target)) {
            currentValue = target;
            clearInterval(interval);
        }
        
        // update displayed value (round)
        $element.text(Math.round(currentValue));
    }, 1000 / steps);
}