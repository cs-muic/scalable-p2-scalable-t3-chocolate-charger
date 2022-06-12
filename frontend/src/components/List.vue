<script>
export default {
  data() {
  	return {
	    parentMessage: 'Parent',
    	items: [{ message: 'Foo' }, { message: 'Bar' }]
  	}
	}
}
</script>


<li v-for="item in items">
  {{ item.message }}
</li>