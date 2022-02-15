<template>
    <div class="flex font-main">
        <DashboardNav/>
        <DashboardMain/>
    </div>
</template>
<script>
export default {
  name: 'DashboardPage',
  middleware: 'auth',
  head: {
    title: 'Exult Bot · Dashboard',
  }
}
</script>