<template>
    <header class="site-header navbar nes-container is-dark">
        <div class="content max-width">
            <div class="nav-brad">
                <p>도봉이와 함께하는 도시정보</p>
            </div>
            <nav>  
                <ul>         
                <li><a href="#" class="nes-btn">Home</a></li>
                <li><a href="#" class="nes-btn">About</a></li>
                <li><a href="#" class="nes-btn">Contact</a></li>
            </ul>     
            </nav>

        </div>

    </header>
</template>

<script>
</script>

<style>
li{
    list-style-type: none;
}

ul{
    display: flex;
}

.site-header.navbar {
    font-family: 'MyWebFont',sans-serif;
}

.site-header .content {
    display: flex;
    height: 70px;
    justify-content: space-between;
    align-items: center;
}

.site-header .content {
    margin: 0 auto;
    padding: 0 10px;
}

.max-width {
    max-width: 1100px;
    width: 100%;
}
</style>
