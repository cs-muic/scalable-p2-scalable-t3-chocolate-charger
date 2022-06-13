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

<div>
	<li v-for="item in items">
  {{ item.message }} 
</li>
</div>
