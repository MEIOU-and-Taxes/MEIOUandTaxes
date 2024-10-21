import os, textwrap

def getTextbox ( name, subname ):
	return textwrap.dedent( f'''\
		custom_text_box = {{
			name = {name}_{subname}
			tooltip = {name}_{subname}_tt
			potential = {{}}
		}}
		''')

def getSlotDefinitions( category_name, frame_number, prod, slot, prevs ):
	name = f'provinceview_tab3_{category_name}{len(prevs)}_{slot}'



	data = f'''\
		#### {prod[ 'name' ]} slot {slot}
		custom_window = {{
			name = {name}_window
			potential = {{
				Prod_HasProd = {{ Prod = {prod[ 'id' ]} }}
				calc_true_if = {{'''
	for prev in prevs:
		data += f'''
					Prod_HasProd = {{ Prod = {prev[ 'id' ]} }} # {prev[ 'name' ]}'''
	data += f'''
					amount = {slot}
				}}
				NOT = {{
					calc_true_if = {{'''
	for prev in prevs:
		data += f'''
						Prod_HasProd = {{ Prod = {prev[ 'id' ]} }} # {prev[ 'name' ]}'''
	data += f'''
						amount = {slot+1}
					}}
				}}
			}}
		}}
		custom_button = {{
			name = {name}
			tooltip = {name}_tt
			potential = {{}}
			trigger = {{}}
			effect = {{}}
			frame = {{ number = {frame_number} trigger = {{ owner = {{ has_country_flag = selected_tab3 }} }} }}
		}}
		'''

	data = textwrap.dedent( data )
	data += getTextbox( name, 'title' )
	for i in range( 1, 5 ):
		data += getTextbox( name, f'text_{i}' )
	return data

def write( dest ):
	categories = [
		{
			"name": "farmlands",
			"prods": [
				{
					"name": "Crops",
					"id": 1
				},
				{
					"name": "Fiber",
					"id": 11
				},
				{
					"name": "Cash Crop",
					"id": 19
				},
				{
					"name": "Spices",
					"id": 20
				},
				{
					"name": "Sericulture",
					"id": 42
				},
				{
					"name": "Dye",
					"id": 12
				},
				{
					"name": "Settled Pasture",
					"id": 7
				},
				{
					"name": "Nomad Pasture",
					"id": 8
				}
			]
		},
		{
			"name": "forestry",
			"prods": [
				{
					"name": "Timber",
					"id": 13
				},
				{
					"name": "Game/Furs",
					"id": 21
				}
			]
		},
		{
			"name": "mines",
			"prods": [
				{
					"name": "Sea Salt",
					"id": 9
				},
				{
					"name": "Rock Salt",
					"id": 10
				},
				{
					"name": "Coal",
					"id": 14
				},
				{
					"name": "Metal",
					"id": 15
				},
				{
					"name": "Rare Metals",
					"id": 16
				},
				{
					"name": "Gold",
					"id": 17
				},
				{
					"name": "Silver",
					"id": 18
				},
				{
					"name": "Marble",
					"id": 41
				}
			]
		},
		{
			"name": "fishery",
			"prods": [
				{
					"name": "Fishery",
					"id": 6
				}
			]
		},
		{
			"name": "industry",
			"prods": [
				{
					"name": "Cottage Industry",
					"id": 38
				},
				{
					"name": "Houseware",
					"id": 24
				},
				{
					"name": "Textile",
					"id": 25
				},
				{
					"name": "Armament",
					"id": 26
				},
				{
					"name": "Ship",
					"id": 27
				},
				{
					"name": "Processed Material",
					"id": 28
				},
				{
					"name": "Silk",
					"id": 33
				},
				{
					"name": "Chinaware",
					"id": 34
				},
				{
					"name": "Carpet",
					"id": 35
				},
				{
					"name": "Glass",
					"id": 36
				},
				{
					"name": "Luxury Cloth",
					"id": 39
				},
				{
					"name": "Steel",
					"id": 40
				}
			]
		},
		{
			"name": "knowledge",
			"prods": [
				{
					"name": "Religious Knowledge",
					"id": 29
				},
				{
					"name": "Higher Learning",
					"id": 30
				}
			]
		},
		{
			"name": "commerce",
			"prods": [
				{
					"name": "Urban Commerce",
					"id": 32
				}
			]
		}
	]

	filename = os.path.basename( __file__ )

	data = ''
	prevs = []
	for idx, category in enumerate( categories ):
		for prod in category[ 'prods' ]:
			for i in range( 0, min( len( prevs )+1, 16 ) ):
				data += getSlotDefinitions( category[ 'name' ], idx+1, prod, i, prevs )
			data += '\n'
			prevs.append( prod )

	dest = os.path.join( dest, 'common', 'custom_gui' )
	os.makedirs( dest, exist_ok=True )
	with open( os.path.join( dest, 'province_industry.txt' ), 'w' ) as f:
		f.write( data )

if __name__ == '__main__':
	write( '.' )
elif __name__ == '__build__':
	write( outdir )
