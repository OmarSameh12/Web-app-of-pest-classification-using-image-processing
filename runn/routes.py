import os.path
import secrets
from keras.utils import load_img, img_to_array
import cv2
import pickle
import numpy as np
import numpy as numpy
from flask import render_template,url_for, flash, redirect, request
from flask_login import login_user, logout_user, login_required,current_user
from PIL import Image
from runn.form import RegistrationForm, LoginForm, predictForm
from runn import app, bcrypt, db, model,mail
from runn.models import User, Image_User, Info
from flask_mail import Message
#model = pickle.load(open('model.pkl','rb'))
temppath=''
result=''

def save_pic(form_picture):
    random_hex=secrets.token_hex(8)
    _,f_ext=os.path.splitext(form_picture.filename)
    picture_name=random_hex+f_ext
    pathFormd=os.path.join(app.root_path,'static/user_pics',picture_name)
    form_picture.save(pathFormd)
    return picture_name,pathFormd
def getinsectname(xclass):
   dicti=  {0: 'Corn Borer', 1: 'Aphids', 2: 'Flea Beetle', 3: 'Legume Blister Beetle', 4: 'Lycroma Delicatula',
                   5: 'Tarnished Plant Bug', 6: 'Adristyrannus', 7: 'Ampelophaga', 8: 'Beet Army Worm',
                   9: 'Beet Weevil', 10: 'Cicadellidae', 11: 'Potosiabre Vitarsis', 12: 'Dacus Dorsalis',
                   13: 'Icerya Purchasi Maskell', 14: 'Lawana Imitata Melichar', 15: 'Locustoidea', 16: 'Lytta Polita',
                   17: 'Pieris Canidia', 18: 'Limacodidae', 19: 'Trialeurodes Vaporariorum', 20: 'Callitettix versicolor',
                   21: 'Luperomorpha Suturalis Chen', 22: 'Brown Plant Hopper', 23: 'Spodoptera Litura', 24: 'Healthy Plant',
                   25: 'Mole Cricket', 26: 'Xylotrechus', 27: 'Black Cutworm', 28: 'Red Spider', 29: 'Oides Decempunctata',
                   30:'Grub'}
   return dicti[xclass]


def send_reset_email(user):
    token=user.get_reset_token()
    msg=Message('BugBust Password Reset',sender="BugBustt@gmail.com",recipients=[user.email],
                body=f'''to reset your password visit the following link: {url_for('reset_password',token=token,_external=True)}  , Please be aware that this link is valid for only one hour and that you also cannot change your password more than once within an hour''')
    mail.send(msg)
@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if (current_user.is_authenticated):
        return redirect(url_for("home"))
    errors=''
    if request.method == "POST":
        name=request.form['username']
        email=request.form['email']
        password=request.form['password']
        user = User.query.filter_by(email=email).first()
        if user:
            errors = "Email already exist"
            return render_template('register.html', errors=errors,flag=0)
        else:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            user = User(name=name, email=email, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            return render_template('register.html',flag=0)
    return render_template("register.html", title="Register",flag=1)

# @app.route("/sort",methods=["GET"])
# def sort():
#     data = db.session.query(Image_User).filter(Image_User.userid == current_user.id)
#     images = []
#     for i in data:
#         images.append(i)
#     sorted_image=sorted(images.created_at)


@app.route("/login", methods=["GET", "POST"])
def login():
    errors=''
    if current_user.is_authenticated:
        return redirect(url_for("profile"))
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        user =User.query.filter_by(email=email).first()
        if user!=None:
            if (user and bcrypt.check_password_hash(user.password,password)):
                print("here")
                login_user(user,remember=True)
                return render_template('login.html',title='login',flag=0)
            else:
                error = "Email or password is incorrect"
                return render_template("login.html", title="Login", errors=error,flag=0)
        else:
            error="Email or password is incorrect"
            return render_template("login.html", title="Login",errors=error,flag=0)

    return render_template("login.html", title="Login",flag=1)

@app.route("/history",methods=["GET"])
@login_required
def history():
        data=db.session.query(Image_User).filter(Image_User.userid==current_user.id)
        images=[]
        for i in data:
            images.append(i)
        information=[]
        for image in images:
            info=Info.query.filter_by(name=image.result).first()
            info.damage=info.damage.replace("'","\\'")
            info.how_to_control=info.how_to_control.replace("'","\\'")
            info.common_name=info.common_name.replace("'","\\'")
            print(info.damage)
            information.append(info)
        unique_info = list(set(information))

        return render_template("historyRes.html",images=images,information=unique_info)

@app.route("/deleteSingleImage/<id>",methods=["POST"])
def deleteSingleImage(id):
    imgid = id
    record = Image_User.query.get_or_404(imgid)
    db.session.delete(record)
    db.session.commit()
    return redirect(url_for("history"))
@app.route("/deleteall",methods=["GET"])
@login_required
def deleteallimages():
    data = db.session.query(Image_User).filter(Image_User.userid == current_user.id).delete(synchronize_session=False)
    db.session.commit()
    return redirect(url_for("history"))


#profile page
@app.route("/profile",methods=["GET","POST"])
def profile():
    print(request.method)
    name=current_user.name
    if request.method=='POST':
        image=request.files['upload']
        #function save_pic automatically saves the image at the folder of user_pic
        image,pathformd=save_pic(image)
        global  temppath
        global  result
        temppath=image
        image = load_img(pathformd, target_size=(224, 224))
        rgb_image = image.convert('RGB')
        image = img_to_array(rgb_image)
        resized_image = image.reshape(1, 224, 224, 3)
        normalized_image = resized_image/255
        predict_x = model.predict(normalized_image)
        resultn = np.argmax(predict_x, axis=1)
        resultc = getinsectname(resultn[0])
        result=resultc
        img_user=Image_User(value=temppath, userid=current_user.id,result=result)
        info =Info.query.filter_by(name=resultc).first()
        str=info.how_to_control
        strings = str.split('.')
        strings=strings[0:-1]
        damage=info.damage
        confidence = predict_x[0][resultn]
        print(confidence)
        threshold = 0.85

        return render_template("results.html",title='result',result=img_user,info=info,string=strings,damage=damage)
    return render_template("profile.html",title="profile",name=name)
@app.route("/save",methods=["GET"])
def save():
    if temppath:
        image_user = Image_User(value=temppath, userid=current_user.id,result=result)
        db.session.add(image_user)
        db.session.commit()
    return redirect(url_for("profile"))


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/reset_password",methods=['POST','GET'])
def reset_password_req():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    if request.method=="GET":
        return render_template("reset_password.html",flag=1)
    else:
        uemail=request.form['email']
        user=User.query.filter_by(email=uemail).first()
        if user:
            send_reset_email(user)
        else:
            return render_template("reset_password.html",flag=0)
        return redirect(url_for("login"))

@app.route("/reset_password/<token>",methods=['GET','POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect("home")
    user=User.verify_reset_token(token)
    if not user:
        return redirect(url_for("reset_password_req",errors="The token is invalid or has been expired"))
    if request.method=='GET':
        return render_template("EnterYourPassword.html")
    else:
        newpass=request.form['pass1']
        hashed_password = bcrypt.generate_password_hash(newpass).decode('utf-8')
        user.password=hashed_password
        db.session.commit()
        return redirect(url_for('login'))

##during dev
@app.route("/createdatabase")
def create_database():
    db.create_all()
    return redirect(url_for("home"))

@app.route("/viewall")
def viewall():
    udata=User.query.all ()
    idata=Image_User.query.all()
    infodata=Info.query.all()
    for user in udata:
         print(user)
    for image in idata:
        print(image)
    for infod in infodata:
       print(infod)
    return redirect(url_for("home"))

@app.route("/deletealltables")
def deleteall():
    db.drop_all()
    return redirect(url_for("home"))

@app.route('/createinfo')
def createinfo():
    db.session.add(Info(name='Corn Borer', common_name='Ostrinia nubilalis',how_to_control="Primary tillage such as chisel plowing or moldboard plowing in the fall can reduce overwintering populations, However, soil and moisture conservation must also be considered when managing insect populations, Mowing corn stalks after harvest can also reduce overwintering populations.Birds may also prey on European corn borer larvae, Overwintering crows will perforate cornstalks and eat overwintering larvae of European corn borer, Red-winged blackbirds will also consume larvae of European corn borer, although they can also damage standing corn.The best pesticide recommendation we can give is to spray with a pyrethroid such as permethrin or bifenthrin every month or so as field crops harden off in mid to late summer.",damage='The boring damage may weaken the plant enough to cause subsequent stalk breakage later in the season, typically occurring below the ear.'))
    db.session.add(Info(name='Red Spider', common_name='spider mite',how_to_control="Spray mineral-free water on the leaves to create a moist environment that will make them disappear, A simple hand-spray is enough for this, Rainwater is a good example, but demineralized water also works.mite-killer that can be found in any garden shop.wipe a soft moist cloth on leaves (topside and underside), Repeat daily until no more red spider mites appear.Beauveria bassiana is a type of fungus that greatly reduces red spider mite fertility and and egg hatching.",damage='Red spiders are a common pest on houseplants and agriculturally important plants, including the foliage and fruit of orchard trees, The mites are sometimes mistaken for small spiders because of their habit of spinning a loose silk webbing on infested plants, A heavy infestation can cause complete defoliation.'))
    db.session.add(Info(name='Aphids', common_name='Greenfly', how_to_control="Try spraying infested plants with a strong stream of water; sometimes all aphids need is a blast to dislodge them,Typically, they are unable to find their way back to the same plant.You can often control aphids by wiping or spraying the leaves of the plant with a mild solution of water and a few drops of dish soap, Soapy water should be reapplied every 2-3 days for 2 weeks.Neem oil, insecticidal soaps, and horticultural oils are effective against aphids, but these substances need to come into contact with the aphids in order to work, Be sure to follow the application instructions provided on the packaging.Diatomaceous earth (DE) is a non-toxic, organic material that will dehydrate aphids.**Warning: Do not apply DE when plants are in bloom, as it will kill pollinators such as bees and butterflies if they come into contact with it.", damage='Aphids seem to find their way into every garden,They are small, soft-bodied insects that feed by sucking the nutrient-rich liquids out of plants;In large numbers, they can weaken plants significantly, harming flowers and fruit and they also multiply quickly.'))
    db.session.add(Info(name='Protaetia', common_name='Oriental Flower Beetle, Asian Flower Beetle', how_to_control='Practices such as crop rotation, removing plant debris after harvest, and maintaining proper sanitation in the garden can help reduce overwintering populations of the pest.Encouraging natural enemies like parasitic wasps and predators such as lacewings and ladybugs can help keep Oriental Flower Beetle populations in check.', damage='A Moderate Damage they rarely cause significant damage to healthy fruit; instead, beetles prefer overripe or already damaged fruits.'))
    db.session.add(Info(name='Flea Beetle', common_name='Potato Flea Beetle, Eggplant Flea Beetle', how_to_control='Remove Garden trash and plow or rototill under weeds to reduce overwintering sites.Introducing natural enemies of flea beetles like parasitic wasps or predatory insects can help keep their populations in check.70% Neem Oil is approved for organic use and can be sprayed on vegetables, fruit trees and flowers to kill eggs, larvae and adult insects. ', damage='Flea beetles chew irregular holes in the leaves.Severe flea beetle damage can result in wilted or stunted plants.'))
    db.session.add(Info(name='Legume Blister Beetle', common_name='Glistening blister beetle', how_to_control='Try spraying infested plants with a strong stream of water; sometimes all aphids need is a blast to dislodge them,Typically, they are unable to find their way back to the same plant.You can often control aphids by wiping or spraying the leaves of the plant with a mild solution of water and a few drops of dish soap, Soapy water should be reapplied every 2-3 days for 2 weeks.Neem oil, insecticidal soaps, and horticultural oils are effective against aphids, but these substances need to come into contact with the aphids in order to work, Be sure to follow the application instructions provided on the packaging.Diatomaceous earth (DE) is a non-toxic, organic material that will dehydrate aphids.', damage='hese beetles can cause significant damage to various plants, including legumes such as beans, peas, and soybeans, They feed on the leaves, stems, flowers, and pods of these plants, resulting in defoliation and reduced crop yield, The larvae of these beetles also feed on plant roots, which can further weaken the plants.'))
    db.session.add(Info(name='Lycroma Delicatula', common_name='Spotted lanternfly', how_to_control='Scraping egg masses :The spotted lanternfly lays its eggs on various surfaces such as tree trunks or outdoor furniture.Methods used to overcome this insect is Chlorpyrifos was found to be effective at killing 100% of eggs.Dinotefuran, imidacloprid, carbaryl, and bifenthrin are effective at controlling the spotted lanternfly.', damage="The spotted lanternfly feeds on a wide range of plants, including fruit trees (such as apple, peach, and grape), hardwood trees (such as maple and oak), and ornamental plants, The insect causes damage by sucking sap from the plant's stems, leaves, and trunks, This feeding activity weakens the plant and can lead to reduced growth, wilting, dieback, and even death in severe cases."))
    db.session.add(Info(name='Tarnished Plant Bug', common_name='Lygus bug', how_to_control='Neonicotinoids are a family of insecticides which cause interference and blockage of the nicotinergic pathway in the central nervous system of insects.Practices such as crop rotation, removing weed hosts near cultivated areas, and maintaining good plant health can help reduce TPB populations.Parasitic wasps, Peristenus digoneutis, were imported from France and their establishment [clarification needed] in the northeastern United States has resulted in reduction of crop losses to the TPB of up to 63% in alfalfa and 65% in apples (biological method).', damage='-	It has piercing-sucking mouthparts and has become a serious pest on small fruits and vegetables in North America, It is considered a highly polyphagous species and feeds on over half of all commercially grown crop plants, but favors cotton, alfalfa, beans, stone fruits, and conifer seedlings, Although it is known to feed on almost all commercial crops, it specifically prefers to feed on young apples and weeds.'))
    db.session.add(Info(name='Adristyrannus', common_name='Eudocima tyrannus', how_to_control='Prevention by means of netting or bagging the fruit is by far the most effective weapon against fruit piercing moth.The other main option of pest control is nightly inspections of targeted fruit trees with a strong torch to spot them as they feed then plucking them off and dispatching of them with a standard squish.', damage="-	Eudocima tyrannus is a moth of the family Erebidae, It is found in south-eastern Siberia, India, eastern China, the Philippines and Japan, it's habitat at Mid-altitude mountain, The adult is considered an agricultural pest, causing damage to many fruit crops by piercing it with its strong proboscis in order to suck the juice."))
    db.session.add(Info(name='Ampelophaga', common_name='Longhorn beetles or round-headed borers', how_to_control='Infested areas should be quarantined to prevent the movement of infested wood materials that may contain beetle larvae or eggs.Tree removal: Infested trees should be removed and destroyed to prevent further spread of the beetles.Insecticides can be used to control adult beetles when they are active on the bark surface during their feeding period, However, this method may not be effective for larvae inside the tree.Natural enemies such as parasitoid wasps have been studied as potential biological control agents for Ampelophaga beetles.', damage="The Asian long-horned beetle is an invasive pest that primarily attacks hardwood trees, including maple, birch, willow, elm, and poplar. Damage caused by Ampelophaga beetles includes tunneling into tree trunks and branches, which disrupts the flow of water and nutrients within the plant, This can lead to tree decline, branch breakage, and eventually tree death if left untreated."))
    db.session.add(Info(name='Beet Army Worm', common_name='Garden Armyworm, Small Mottled Willow Moth', how_to_control='Pheromone traps and mechanical hand picking of adults and caterpillars are extensively used. Eggs can be killed by using petroleum oil concentrations.Applying cottonseed oil to leaves can eliminate both eggs and larvae.', damage='This pest is known for its voracious appetite and ability to cause significant damage to a wide range of plants.Damage caused by the Beet Army Worm can vary depending on the stage of the plant it attacks, In young seedlings, it may consume entire leaves or bore into stems, causing wilting or death, On mature plants, it typically feeds on foliage, leaving irregular holes and skeletonized leaves, Additionally, it can also attack fruits and flower.'))
    db.session.add(Info(name='Beet Weevil', common_name='Strawberry Root Weevil , Black Vine Weevil', how_to_control="Crop rotation, early sowing and promotion of youth development; do not plant beets directly next to previous year's beet or alfalfa field.Draw trap grooves in stands after sugar beet as well as in this year's sugar beet plots.Seeding this year's sugar beet areas with pheromone traps after the beetle has emigrated from the old areas.Combination of dressed seed with multiple spray applications.", damage="The pest causes marginal or pitting damage to the leaves of young beet plantlets, In the cotyledon stage of sugar beet, the beet root weevil can cause bare root feeding at densities as low as one beetle per square meter..In Austria's sugarbeet-growing regions, the beet root weevil is one of the most economically significant pests, Since the mortality of beet root weevil increases at low temperatures and high soil moisture, low precipitation and high average favor the development of the beet root weevil."))
    db.session.add(Info(name='Cicadellidae', common_name='Leafhoppers, Sharpshooters',how_to_control='Remove garden trash and other debris shortly after harvest to reduce over-wintering sites.Floating row covers can be used as a physical barrier to keep leafhoppers from damaging plants.Commercially available beneficial insects, such as ladybugs, lacewing and minute pirate bugs, are all voracious predators of both the egg and young larval stage.Apply diatomaceous earth to plants and/or spot treat with insecticidal soap to keep pest populations under control, Thorough coverage of both upper and lower infested leaves is   necessary for effective control.BotaniGard ES is a highly effective biological insecticide containing Beauveria bassiana, an entomopathogenic fungus that attacks a long-list of troublesome crop pests – even resistant strains! Weekly applications can prevent insect population explosions and provide protection equal to or better than conventional chemical pesticides.If pest levels become intolerable, spot treat with potent, fast-acting organic insecticides as a last resort.',damage=''))
    db.session.add(Info(name='Dacus Dorsalis', common_name='Oriental fruit fly', how_to_control=' Organic Control: Use bait sprays with a suitable organically accepted insecticide (e,g,, Spinosad) mixed with a protein bait and Install pheromone traps to monitor fly number.Chemical Control: Use baits with a suitable insecticide (e,g, malathion) mixed with a protein solution, The most widely protein used is the hydrolysed form, but some of these are highly phytotoxic, Light-activated xanthene dye is an effective alternative, The males of B, dorsalis are attracted to methyl eugenol (4-allyl-1,2-dimethoxybenzene), sometimes in very large numbers.Preventive Measures:Chose resilient varieties, if available in your area, Destroy unmarketable and infested fruits, Rake or disturb the soil below the fruit trees to disturb the pupae, Wrap the fruit before maturation, either in newspaper, a paper bag, or polythene sleeve.', damage="Dacus dorsalis is a significant pest of various fruits, including mangoes, papayas, citrus, guavas, and melons, The larvae of Dacus dorsalis feed on the fruits, causing damage such as premature fruit drop, fruit rot, and reduced fruit quality.The larval stage of the life cycle is the most damaging to fruits because of larval feeding on the soft flesh of fruits, After ovipositing occurs by a female fly, the larvae develop under the skin of the fruit or soft tissues of the plant and begin to feed on the fruit or plant's flesh."))
    db.session.add(Info(name='Icerya Purchasi Maskell', common_name=' Cottony cushion scale', how_to_control='Chemical Control: The insect growth regulator pyriproxyfen has been found to be as effective in controlling I, purchasi, Good control was achieved when applied alone or with 0,5% mineral oil, Another growth regulator, buprofezin, gave 100% mortality of crawlers and 31% decreased egg hatch when the adults were sprayed with it.Biological Control : By natural enemies:The parasitoid Cryptochaetum iceryae has also proved to be effective in regulating I, purchasi populations, Adult C, iceryae are sensitive to heat and aridity and are most effective in regulating cottony cushion scale populations in cooler coastal areas, In more arid and hot inland areas, vedalia beetles are more effective.', damage='Icerya purchasi is a significant pest of various plants, including citrus, ornamental plants, and woody shrubs. I, purchasi extracts significant quantities of sap from the host plant, Damage is mostly caused by sap depletion; the shoots dry up; defoliation occurs and branches or whole trees may die, Copious honeydew excreted by the scales coats the leaves, resulting in sooty mold growth, which blocks light and air from the leaves, This reduces photosynthesis and the productivity of fruit and forest trees, and disfigures ornamental plants and fruit.'))
    db.session.add(Info(name='Lawana Imitata Melichar', common_name='White moth bug/Whitefly', how_to_control='Consider spraying your plants’ leaves with insecticidal soap.Use spray (horticultural) oils to control whiteflies minimizing adverse effects on natural enemies.Prune away severely infested portions of the plant, The removed material should be placed and sealed in plastic bags and removed from the property, Dispose of properly and do not compost.', damage='Whiteflies can seriously injure plants by sucking juices from them, causing leaves to yellow, shrivel, and drop prematurely, If the numbers of whiteflies per leaf are great enough, it could possibly lead to plant death.'))
    db.session.add(Info(name='Locustoidea', common_name='Desert locust', how_to_control="Till the garden soil from mid- to late summer to eliminate areas where females lay their eggs, These eggs overwinter in the soil and hatch in the spring, Till the ground again in late fall and early spring to destroy the eggs that were laid the previous summer.Cultural Control: Eliminate weeds even in areas that don't have garden plants to reduce the availability of food for newly hatched nymphs, Good weeding practice goes a long way toward reducing overall grasshopper populations. Chemical Control: Carbaryl is the most effective chemical pesticide on grasshoppers, but unfortunately, this chemical is also highly toxic to beneficial insects, Baits containing carbaryl are safer than sprays when it comes to protecting bees and other beneficial insects, but even baits should be used very carefully and only in areas where you know grasshoppers are feeding.Biological Control: Nosema locustae and Beauveria bassiana, fungi that affect the digestion of grasshoppers.", damage='Grasshoppers are herbivores that feed on grasses and the leaves and stems of plants, The symptom of grasshopper damage is much the same as for other gnawing insects: ragged and chewed holes in the leaves, stems, and fruit of plants.'))
    db.session.add(Info(name='Lytta Polita', common_name='Colorado potato beetle', how_to_control='It is important to use harvest equipment that allows the beetles to escape from mowed and swathed forage because the type of equipment and its operation has an impact on blister beetle mortality during hay harvest (Mechanical/Physical Control).The insecticides thiodicarb, chlorpyriphos, quinalphos and cypermethrin significantly reduce the blister beetle population, (Chemical Control).Pigweed (Amaranthus spp,) is highly attractive to adult beetles, Keep it out of your landscape entirely.Hand-picking can be effective in-home gardens, particularly when their numbers are low, But never handle blister beetles with bare hands, Always wear gloves.', damage='The damage caused by Lytta polita includes defoliation, where the beetles consume the leaves of the plants, leading to reduced photosynthesis and stunted growth, Severe infestations can result in complete defoliation, which can significantly impact crop yields.'))
    db.session.add(Info(name='Pieris Canidia', common_name='Cabbage white butterfly', how_to_control='Cultural control: Practices such as crop rotation, intercropping with repellent plants, Additionally, covering plants with netting or row covers can prevent adult butterflies from laying eggs on the plants.Integrated Pest Management (IPM): Implementing an integrated approach that combines multiple control methods is often the most effective way to manage Pieris canidia, This involves monitoring butterfly populations, using cultural and mechanical control methods as the first line of defense.Natural pyrethrins (this is a natural pesticide found in flowers).Bacillus Thuringiensis Bacteria (it has an effective treatment for the plants).', damage='-	The damage caused by Pieris canidia includes feeding on the leaves of the plants, resulting in large irregular holes and skeletonized leaves, Severe infestations can lead to reduced plant growth and yield.'))
    db.session.add(Info(name='Limacodidae', common_name='Slug caterpillars or cup moths', how_to_control='Neem Oil is a natural insecticide used to get rid of caterpillars.', damage='They are dangerous pests as they can do severe reactions to humans.They affect the coconut palm, banana palm, African oil palm, mango, coffee, tea and mangrove palm.They feed on the leaves of the plants, the first instar caterpillars form windows in leaves while the matures feed from the outer edges of leaves.'))
    db.session.add(Info(name='Trialeurodes Vaporariorum', common_name='Glasshouse whitefly or greenhouse whitefly', how_to_control='Biopesticides such as Lecanicillium muscarium that complement these natural enemies.Beneficial insects such as the aphelinid parasitoid.', damage='They damage the plants through feeding on the leaves and extract their nourishment, they have the ability to transmit several plant viruses through different plants.'))
    db.session.add(Info(name='Callitettix versicolor', common_name='Sugarcane spittle bug, Rice spittle bug, Black froghopper', how_to_control='Physically remove them by hand.Spray them with water.Put the plants away from weeds as they are one of their food sources.Pesticides are not effective against these pests as the nymphs are protected inside their spittle masses.', damage='They feed on ornamental grasses, roses, chrysanthemums, clover, strawberries, herbs and many other garden plants.They are known for the frothy spittle mass they produce while feeding on plants.Spittlebug nymphs penetrate the plant stems and suck plant juices.In most cases, spittlebug feeding is not damaging to plants but If too many spittlebugs are present, feeding can cause leaves to lose their shape.'))
    db.session.add(Info(name='Luperomorpha Suturalis Chen', common_name='Striped flea beetle', how_to_control='The use of entomopathogenic nematodes (EPNs) within an integrated pest management approach may offer an effective and environmentally safe strategy to suppress outbreaks of this pest.Dusting leaves with plain talcum powder that repels these pests.Use white sticky traps to capture the pests as they jump.', damage='The larvae feed on fine roots and root hairs, and eventually pupate in the soil, The pupal stage takes about seven days, The adults feed on the above-ground parts of the plants, leaving a distinct “shot-hole” pattern on leaves, and snap the stems of seedlings.'))
    db.session.add(Info(name='Brown Plant Hopper', common_name='', how_to_control="Use light traps at night when rice is prone to planthopper attack, Do not place lights near seedbeds or fields, If the light trap is inundated with hundreds of BPH,it's a signal to check your seedbed or field immediately.If natural enemies out-number BPH the risk of hopperburn is low,Natural enemies of BPH include water striders, mirid bugs, spiders, and various egg parasitoids.Flood the seedbed, for a day, so that only the tips of seedlings are exposed will control BPH. Only apply insecticides to the seedbed, for BPH or WBPH, if all of these conditions are met: an average of more than one planthopper per stem,on average, more planthoppers than natural enemies,flooding the seedbed is not an option.", damage="These insects are among the most important pests of rice, which is the major staple crop for about half the world's population, They damage rice directly through feeding and also by transmitting two viruses, rice ragged stunt virus and rice grassy stunt virus, Up to 60% yield loss is common in susceptible rice cultivars attacked by the insect."))
    db.session.add(Info(name='Spodoptera Litura', common_name='Tobacco Cutworm, Cluster Caterpillar, and Cotton Leafworm', how_to_control='•	Bacillus Thuringiensis Bacteria that effectively control the pests.Planting resistant plants such as groundnuts.Planting near derris and garlic plants.Controlling this pest focuses on using the fungus Nomuraea rileyi on the larval stage of this moth,.Adults can be collected with sex pheromone-baited traps (males) or light traps (males and females).', damage='-	They can cause severe defoliation, skeletonization of leaves, and damage to flowers and fruits, This can result in reduced plant growth, yield loss, and even plant death in severe infestations'))
    db.session.add(Info(name='Healthy Plant', common_name='', how_to_control='', damage=''))
    db.session.add(Info(name='Mole Cricket', common_name='African mole cricket', how_to_control='If you suspect mole crickets, a simple soapy-water flush brings them to the surface and confirms your suspicions, If your soil is dry, water it well, Mole crickets stay deeper in dry soil, but moisture brings them higher.For successful control, pesticides must be able to reach mole crickets in their protective, sub-surface tunnels. Ideal treatments also expand your coverage window as nymphs hatch and start to feed.', damage='-	It damages cereals, legumes, perennial grasses, potatoes, vegetable crops, beet, sunflower, tobacco, hemp, flax and strawberry, It also is troublesome in nurseries where young plants may be killed, and damages the roots of vines, fruit and other trees.'))
    db.session.add(Info(name='Xylotrechus', common_name='Longhorn beetle', how_to_control='It is important to monitor plants regularly for signs of damage, such as exit holes, sawdust-like frass, or wilting branches.2-	If an infestation is detected, appropriate control measures can be taken, such as pruning and removing affected branches, applying insecticides targeted at the larvae or adults, or using biological control methods.', damage='The damage caused by Xylotrechus on plants can vary depending on the specific species and the severity of the infestation, Xylotrechus is a genus of longhorn beetles that can attack various types of trees, including fruit trees, ornamental trees, and forest trees, this can result in defoliation, reduced photosynthesis, and increased vulnerability to other pests and diseases.'))
    db.session.add(Info(name='Black Cutworm', common_name='', how_to_control='Seed treatments: High rates of neonicotinoid seed treatments (Poncho, Cruiser, Gaucho) are very effective on many seed and seedling insects and they can provide some protection against black cutworm, They may not always provide satisfactory cutworm control,  Seed-applied diamide insecticides (chlorantaniliprole) can also affect black cutworm larvae.Insecticides: cutworms are controlled well with rescue insecticide applications and many post-plant insecticide products provide effective control of black cutworms,Several compounds within the pyrethroid, organophosphate, carbamate, and diamide groups.', damage='Black Cutworms are known for their damage on various plants, particularly corn, soybeans, and other vegetables, They feed on the stems of young plants, often cutting them off near the soil surface, This can lead to plant death or stunted growth.'))
    db.session.add(Info(name='Oides Decempunctata', common_name='Ten-spotted Lady Beetle', how_to_control='Ten-spotted Lady Beetle is generally considered beneficial and should not be targeted for control unless it becomes a significant pest itself.', damage='The damage caused by Oides Decempunctata is primarily associated with its feeding behavior. In some cases, these lady beetles may feed on plant tissues, causing small holes or punctures in leaves; However, this damage is usually minimal and does not significantly impact plant health.'))
    db.session.add(Info(name='Grub', common_name='', how_to_control='Limit moisture, Grubs need moisture to survive and thrive;As such, one easy way to decrease their numbers is to create an artificial drought.Use milky spore, Milky spore is a bacterial disease that targets the larval stage of Japanese beetles,  its also n eco-friendly, non-toxic, natural option and an excellent way to control white grub populations.Make a grub killer with borax, Borax is a common household cleaning ingredient that can be used to kill grubs.', damage='White grubs eat organic matter, including the roots of plants.Grubs feed on the roots of plants, causing significant damage to lawns, gardens, and agricultural crops.Feeding by grubs can lead to wilting, yellowing, or browning of plants.Affected plants may become weak and easily uprooted due to the loss of root support.Damage is often most severe in late summer and early fall.'))
    db.session.commit()

    return redirect(url_for('home'))
