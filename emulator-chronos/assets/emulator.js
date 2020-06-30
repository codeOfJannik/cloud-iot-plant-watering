const Emulator = {
	pollInterval: 1000
};

Vue.component("gpio-led", {
	props: ["id"],
	data: function() {
		return {
			gpio: {
				state: {
					color: "green"
				}
			}
		};
	},
	template: `
	<div class="gpio" :id="id">
		<svg version="1.1" baseProfile="full" class="icon" xmlns="http://www.w3.org/2000/svg" width="100" height="60" viewBox="-50 -30 100 60">
		  <defs>
    		<filter id="blur" x="-100%" y="-100%" width="300%" height="300%">
      		<feGaussianBlur in="SourceGraphic" stdDeviation="5" />
    		</filter>
  		</defs>
	  	<rect width="100%" height="100%" fill="transparent" />

	  	<circle cx="-30" cy="0" r="5" fill="#09be66" />
			<line x1="0" y1="0" x2="-30" y2="0" style="stroke:rgb(100,100,100);stroke-width:4;" stroke-linecap="round" />
	  	
			<circle cx="30" cy="0" r="5" fill="#09be66" />
			<line x1="0" y1="0" x2="30" y2="0" style="stroke:rgb(100,100,100);stroke-width:4;" stroke-linecap="round" />

	  	<circle cx="0" cy="0" r="20" :fill="gpio.state.color" filter="url(#blur)" v-if="gpio.state.on" />
	  	<circle cx="0" cy="0" r="20" fill="rgba(0,0,0,0.2)" filter="url(#blur)" v-else />
	  	<circle cx="0" cy="0" r="14" :fill="gpio.state.color" />
	  	<circle cx="0" cy="0" r="14" fill="rgba(255,255,255,0.5)" />
	  	<circle cx="0" cy="0" r="12" :fill="gpio.state.color" />
	  	<circle cx="0" cy="0" r="12" fill="rgba(255,255,255,0.3)" v-if="gpio.state.on" />
	  	<circle cx="-3" cy="-3" r="5" fill="rgba(255,255,255,0.3)" v-if="!gpio.state.on" />
		</svg>
		<div class="id">{{ id }}</div>
	</div>
	`,
	created: function() {
		setInterval(this.reload, Emulator.pollInterval);
		this.reload();
	},
	methods: {
		reload: function() {
			fetch("gpios/" + this.id)
				.then(response => {
					return response.json();
				})
				.then(data => {
					this.gpio = data;
				});
		}
	}
});

Vue.component("gpio-switch", {
	props: ["id"],
	data: function() {
		return {
			gpio: {
				state: {}
			}
		};
	},
	template: `
	<div class="gpio" :id="id">
		<svg version="1.1" baseProfile="full" class="icon" xmlns="http://www.w3.org/2000/svg" width="100" height="60" viewBox="-50 -30 100 60">
		  <defs>
    		<filter id="blur" x="-100%" y="-100%" width="300%" height="300%">
      		<feGaussianBlur in="SourceGraphic" stdDeviation="5" />
    		</filter>
  		</defs>

	  	<circle cx="-40" cy="20" r="5" fill="#09be66" />
	  	<line x1="-40" x2="-15" y1="20" y2="20" stroke="#09be66" stroke-width="2" stroke-linecap="round" />
	  	<line x1="-15" x2="-15" y1="0" y2="20" stroke="#09be66" stroke-width="2" stroke-linecap="round" />
	  	
			<circle cx="40" cy="20" r="5" fill="#09be66" />
	  	<line x1="40" x2="15" y1="20" y2="20" stroke="#09be66" stroke-width="2" stroke-linecap="round" />
	  	<line x1="15" x2="15" y1="0" y2="20" stroke="#09be66" stroke-width="2" stroke-linecap="round" />

	  	<rect width="50" height="30" x="-25" y="-15" rx="5" fill="rgb(50,50,50)" filter="url(#blur)" />
	  	<rect width="50" height="30" x="-25" y="-15" rx="5" fill="rgb(60,60,60)" />
	  	<rect width="40" height="16" x="-20" y="-8" rx="2" fill="rgb(30,30,30)" />

			<g :transform="'translate(' + switchPosition() + ',0)'">
	  		<rect width="14" height="12" y="-6" rx="2" fill="rgb(70,70,70)" />
	  		<rect width="2" height="10" x="4" y="-5" fill="rgb(85,85,85)" />
	  		<rect width="2" height="10" x="8" y="-5" fill="rgb(85,85,85)" />
			</g>

			<text x="30" text-anchor="start">on</text>
			<text x="-30" text-anchor="end">off</text>
	  	
			<rect class="action" x="-50%" y="-50%" width="100%" height="100%" fill="transparent" v-on:click="toggle" />
		</svg>
		<div class="id">{{ id }}</div>
	</div>
	`,
	created: function() {
		setInterval(this.reload, Emulator.pollInterval);
		this.reload();
	},
	methods: {
		reload: function() {
			fetch("gpios/" + this.id)
				.then(response => {
					return response.json();
				})
				.then(data => {
					this.gpio = data;
				});
		},
		switchPosition: function() {
			if (this.gpio.state.open) {
				return -17;
			}
			return 4;
		},
		toggle: function() {
			fetch("gpios/" + this.id, {
				method: "POST",
				headers: {
					"Content-Type": "application/json"
				},
				body: JSON.stringify({ open: !this.gpio.state.open })
			})
				.then(response => {
					return response.json();
				})
				.then(data => {
					this.gpio = data;
				});
		}
	}
});

Vue.component("gpio-sensor", {
	props: ["id"],
	data: function() {
		return {
			gpio: {
				state: {}
			}
		};
	},
	template: `
	<div class="gpio sensor" :id="id">
		<svg version="1.1" baseProfile="full" class="icon" xmlns="http://www.w3.org/2000/svg" width="160" height="60" viewBox="-80 -30 160 60">
		  <defs>
    		<filter id="blur" x="-100%" y="-100%" width="300%" height="300%">
      		<feGaussianBlur in="SourceGraphic" stdDeviation="5" />
    		</filter>
  		</defs>


	  	<circle cx="-40" cy="20" r="5" fill="#09be66" />
	  	<line x1="-40" x2="-15" y1="20" y2="20" stroke="#09be66" stroke-width="2" stroke-linecap="round" />
	  	<line x1="-15" x2="-15" y1="0" y2="20" stroke="#09be66" stroke-width="2" stroke-linecap="round" />
	  	
			<circle cx="40" cy="20" r="5" fill="#09be66" />
	  	<line x1="40" x2="15" y1="20" y2="20" stroke="#09be66" stroke-width="2" stroke-linecap="round" />
	  	<line x1="15" x2="15" y1="0" y2="20" stroke="#09be66" stroke-width="2" stroke-linecap="round" />
			
			<circle cx="0" cy="20" r="5" fill="#09be66" />
	  	<line x1="0" x2="0" y1="20" y2="20" stroke="#09be66" stroke-width="2" stroke-linecap="round" />

	  	<rect width="120" height="32" x="-60" y="-16" rx="5" fill="rgb(50,50,50)" filter="url(#blur)" />
	  	<rect width="120" height="32" x="-60" y="-16" rx="5" fill="rgb(60,60,60)" />
	  	<rect width="80" height="22" x="-40" y="-11" rx="2" fill="rgb(30,30,30)" />
			
			<text class="display" y="1" text-anchor="middle">{{ gpio.state.value }}{{ gpio.state.unit }}</text>

			<text class="button" x="50" y="1" text-anchor="middle">+</text>
			<text class="button" x="-50" y="1" text-anchor="middle">-</text>

	  	<rect class="action" x="0" y="-50%" width="50%" height="100%" fill="transparent" v-on:click="increase" />
	  	<rect class="action" x="-50%" y="-50%" width="50%" height="100%" fill="transparent" v-on:click="decrease"/>
		</svg>
		<div class="id">{{ id }}</div>
	</div>
	`,
	created: function() {
		setInterval(this.reload, Emulator.pollInterval);
		this.reload();
	},
	methods: {
		reload: function() {
			fetch("gpios/" + this.id)
				.then(response => {
					return response.json();
				})
				.then(data => {
					this.gpio = data;
				});
		},
		decrease: function() {
			this.change(this.gpio.state.value - this.gpio.state.increment);
		},
		increase: function() {
			this.change(this.gpio.state.value + this.gpio.state.increment);
		},
		change: function(value) {
			fetch("gpios/" + this.id, {
				method: "POST",
				headers: {
					"Content-Type": "application/json"
				},
				body: JSON.stringify({ value: value })
			})
				.then(response => {
					return response.json();
				})
				.then(data => {
					this.gpio = data;
				});
		}
	}
});

window.addEventListener("DOMContentLoaded", event => {
	new Vue({ el: "#app" });
});
