import random
import os
from faker import Faker
from PIL import Image
from django.core.management.base import BaseCommand
from NFTapp.models import User, NFTProduct, Topic, OwnerNFTProduct, Author, Type
from NFT.settings import MEDIA_ROOT
fake = Faker()

def run():
    User.objects.all().delete()
    username_superuser = 'duc'
    email_superuser = 'duc@fgmail.com'
    password_superuser = 'duc123'

    User.objects.create_superuser(username_superuser, email_superuser, password_superuser)
    print("USER:")
    user_obj_list = []
    for _ in range(30):
            data = {
                "name": fake.name(),
                "email": fake.email(),
                "username": fake.email().split('@')[0],
                "password":fake.password(),
                "bio": fake.text(max_nb_chars=300),
                "creator": random.choice([True, False]),
            }
            # user, _ = User.objects.get_or_create(**data)
            user = User.objects.create(**data)
            print(f"\tSuccessfully created user with info {user.name}, {user.email}, {user.bio} {user.creator}")
            user_obj_list.append(user)

    # Load type obj
    print("----------------------------------------------------------------")
    print("TYPE:")
    Type.objects.all().delete()
    types = ['artworks', 'collections']
    type_obj_list = []
    for type in types:
        data = {
            "name": type
        }
        # type_obj, _ = Type.objects.get_or_create(**data)
        type_obj = Type.objects.create(**data)
        type_obj_list.append(type_obj)
        print(f"\tSuccesfully created type {type}")

    # Load topic obj
    print("----------------------------------------------------------------")
    print("TOPIC:")
    Topic.objects.all().delete()
    topics = ['Alternate Medium Space', 'KittyMotions', 'Digital Fashion World']
    topic_obj_list = []
    for topic in topics:
        data = {
            "name": topic
        }
        # topic_obj, _ = Topic.objects.get_or_create(**data)
        topic_obj = Topic.objects.create(**data)
        topic_obj_list.append(topic_obj)
        print(f"\tSuccesfully created topic {topic}")

    # Load author obj
    print("----------------------------------------------------------------")
    print("AUTHOR:")
    Author.objects.all().delete()
    authors = [user.name for user in User.objects.all() if user.creator]
    author_obj_list = []
    for author in authors:
        data = {
            "name": author
        }
        # author_obj, _ = Author.objects.get_or_create(**data)
        author_obj = Author.objects.create(**data)
        author_obj_list.append(author_obj)
        print(f"\tSuccesfully created author {author}")

    # Load nft product
    print("----------------------------------------------------------------")
    print("Product:")
    NFTProduct.objects.all().delete()
    nft_names = [
        "EtherGems", "CryptoCanvas", "DigitalDreamscapes", "PixelPioneers", "CryptoCollectibles", 
        "ArtBlockChain", "NFTNova", "DecentralizedVisions", "VirtualVogue", "TechnoTreasuries", 
        "MetaMasterpieces", "BitArtGallery", "EtherIcons", "NeonNomads", "CryptoCraftworks", "NFTUniverse", 
        "DigitalDynasty", "BlockchainBrushstrokes", "PixelPrestige", "EtherEnigmas", "CodeCanvas", 
        "CryptoChronicles", "VirtualVagabonds", "BitBliss", "NFTNirvana", "ArtisticAlgorithms", "CryptoCuriosities", 
        "EtherEssence", "BitstreamBoulevard", "NFTNocturnes"
    ]
    nft_prices = [round(random.uniform(0, 10), 2) for _ in range(30)]
    nft_quantity = [random.randint(0, 20) for _ in range(30)]
    nft_image_files = {}
    explore_dir = os.path.join(MEDIA_ROOT, "explore")

    for dir in os.listdir(explore_dir):
        inside_dir = os.path.join(explore_dir, dir)
        for dir_2 in os.listdir(inside_dir):
            nft_image_files.update({dir_2: []})
            inside_dir_file = os.path.join(inside_dir, dir_2)
            for file in os.listdir(inside_dir_file):
                nft_image_files[dir_2].append(os.path.join(inside_dir_file, file).replace("\\", "//"))
    # [print(k, v) for k, v in nft_image_files.items()]

    cnt = 1
    nft_product_obj_list = []
    for k, v in nft_image_files.items():
        data={}
        if k.startswith("collection"):
            data.update({"type": type_obj_list[0]})
        else: 
            cnt = 1
            data.update({"type": type_obj_list[1]})
        for image in v:  
            data = {
                "name": random.choice(nft_names),
                "price": random.choice(nft_prices),
                "author": random.choice(author_obj_list),
                "image": image,
                "topic": random.choice(topic_obj_list),
                "quantity": random.choice(nft_quantity),
                "description": fake.text(max_nb_chars=300),
                "stars": random.randint(0, 5),
                "artwork": cnt
            }
            # nft_product_obj, _ = NFTProduct.objects.get_or_create(**data)
            nft_product_obj = NFTProduct.objects.create(**data)
            nft_product_obj_list.append(nft_product_obj)
            print(f"\tSuccesfully created product with info {nft_product_obj.name} {nft_product_obj.price} {nft_product_obj.image} {nft_product_obj.quantity} {nft_product_obj.description} {nft_product_obj.stars} {nft_product_obj.artwork}")
            cnt += 1
    # import svgwrite

    # svg_file_path = nft_image_files['artworks_1'][0]

    # dwg = svgwrite.Drawing(svg_file_path)

    # with open(svg_file_path, "r") as svg_file:
    #     svg_content = svg_file.read()
    #     print(svg_content)
    # print(nft_image_files)

    # Load owner of a nft product
    print("----------------------------------------------------------------")
    for user in user_obj_list:
        for i in range(random.randint(3, 5)):
            data = {
                "owner": user,
                "product": random.choice(nft_product_obj_list)
            }
            # owner_nft_product, _ = OwnerNFTProduct.objects.get_or_create(**data)
            owner_nft_product = OwnerNFTProduct.objects.create(**data)
            print(f"\tUser with uuid {data['owner'].id} owns the nft product with uuid {data['product'].id}")
    