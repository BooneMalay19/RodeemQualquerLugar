// Seleciona o elemento de vídeo principal do YouTube
const video = document.querySelector('video');

// Se o vídeo for encontrado
if (video) {
    // ⚙️ Esconde apenas o vídeo (mantém controles e player)
    video.style.visibility = 'hidden'; // Invisível
    video.style.pointerEvents = 'none'; // Não clicável

    // ⚙️ Cria o iframe do jogo (stream local)
    const iframe = document.createElement('iframe');
    iframe.src = 'http://127.0.0.1:8080/video_feed'; // Link do stream Flask

    // Estilo do iframe (sem barras e tamanho exato)
    iframe.style.position = 'absolute auto';
    iframe.style.border = 'none'; // Sem borda
    iframe.style.overflow = 'hidden'; // Remove qualquer barra dentro do iframe
    iframe.style.width = '900px'; // Tamanho exato do vídeo
    iframe.style.height = '800px'; // Tamanho exato do vídeo
    iframe.style.marginTop = '10%'; // Tamanho exato do vídeo
    iframe.style.zIndex = '-70%'; // Em cima do vídeo

    // ⚙️ Função pra posicionar o iframe no lugar do vídeo
    const positionIframe = () => {
        const rect = video.getBoundingClientRect();
        iframe.style.top = rect.top + window.scrollY + 'px';
        iframe.style.left = rect.left + window.scrollX + 'px';
    };

    // ⚙️ Posiciona inicialmente
    positionIframe();

    // ⚙️ Observa mudanças no tamanho do player (modo cinema, tela cheia)
    const observer = new ResizeObserver(positionIframe);
    observer.observe(video.parentElement); // Observa o container

    // ⚙️ Atualiza em caso de rolagem ou resize
    window.addEventListener('scroll', positionIframe);
    window.addEventListener('resize', positionIframe);

    // ⚙️ Insere o iframe no mesmo container do vídeo
    video.parentElement.appendChild(iframe);

    console.log('✅ Jogo sobreposto ao player, sem barras e tamanho correto!');
} else {
    console.log('❌ Vídeo do YouTube não encontrado.');
}