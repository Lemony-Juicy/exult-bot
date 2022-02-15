<template>
    <div class="flex font-main">
        <DashboardNav/>
        <DashboardModules/>
    </div>
</template>
<script>
export default {
  name: 'DashboardModulesPage',
  middleware: 'auth',
  head: {
    title: 'Exult Bot · Modules',
  }
}
</script>