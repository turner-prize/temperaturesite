<script>
import { Line } from 'vue-chartjs'

export default {
  extends: Line,
  props: ['chartdata','options','title'],
  mounted () {
    this.renderChart(this.chartdata, this.options,this.title)
  }
}
</script>