<template>
    <div class="flex font-main">
        <DashboardNav/>
        <DashboardSettings/>
    </div>
</template>

<script>
export default {
  name: 'DashboardSettingsPage',
  middleware: 'auth',
  head: {
    title: 'Exult Bot · Settings',
  }
}
</script>
