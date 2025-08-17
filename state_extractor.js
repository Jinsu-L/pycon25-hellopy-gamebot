(() => {
    if (window.__pyson_bot_injected__) return;
    window.__pyson_bot_injected__ = true;
    
    const ctxp = CanvasRenderingContext2D.prototype;
    const drawLogs = [];
    
    // drawImage 후킹
    const origDrawImage = ctxp.drawImage;
    ctxp.drawImage = function(img, x, y, w, h) {
        let type = '';
        try {
            if (img && img.src) {
                if (img.src.includes('py_0.png')) {
                    type = 'snake';
                } else if (img.src.includes('py_jogak')) {
                    type = 'food';
                }
            }
        } catch (e) {}
        
        if (type) {
            drawLogs.push({ 
                type: type, 
                x: Math.round(x), 
                y: Math.round(y), 
                w: w || 60, 
                h: h || 60 
            });
        }
        
        return origDrawImage.apply(this, arguments);
    };
    
    // 상태 스냅샷 함수
    window.__get_game_state__ = () => {
        const cellSize = 60;
        const cols = 15; // 900 / 60
        const rows = 10; // 600 / 60
        
        const board = Array.from({ length: rows }, () => Array(cols).fill(0));
        const snake = [];
        let food = null;
        
        let score = 0;
        const scoreElement = document.querySelector('#score');
        if (scoreElement) {
            score = parseInt(scoreElement.textContent) || 0;
        }
        
        let gameOver = false;
        const gameOverElement = document.querySelector('#gameOver');
        if (gameOverElement) {
            const style = window.getComputedStyle(gameOverElement);
            gameOver = style.display !== 'none';
        }
        
        drawLogs.forEach(entry => {
            const cx = Math.floor(entry.x / cellSize);
            const cy = Math.floor(entry.y / cellSize);
            
            if (cx >= 0 && cx < cols && cy >= 0 && cy < rows) {
                if (entry.type === 'snake') {
                    board[cy][cx] = 1;
                    snake.push({ x: cx, y: cy });
                } else if (entry.type === 'food') {
                    board[cy][cx] = 2;
                    food = { x: cx, y: cy };
                }
            }
        });
        
        drawLogs.length = 0;
        
        return { 
            board, 
            snake, 
            food, 
            score, 
            gameOver,
            gridWidth: cols,
            gridHeight: rows
        };
    };
    
    console.log('PY-SON Bot state extractor injected successfully');
})();