"""
A Python wrapper for the three.js library
https://threejs.org/docs/index.html

"""
from browser import window, load

load("static/js/three.min.js")
load("static/js/OrbitControls.js")
load("static/js/OBJLoader.js")
load("static/js/FirstPersonControls.js")
load("static/js/FlyControls.js")

THREE = window.THREE

Object3D = THREE.Object3D

PolarGridHelper = THREE.PolarGridHelper.new
AxesHelper = THREE.AxesHelper.new
Euler = THREE.Euler.new

SphereGeometry = THREE.SphereGeometry.new
CubeGeometry = THREE.CubeGeometry.new
CylinderGeometry = THREE.CylinderGeometry.new
BufferGeometry = THREE.BufferGeometry.new
Geometry = THREE.Geometry.new

LineBasicMaterial = THREE.LineBasicMaterial.new
MeshNormalMaterial = THREE.MeshNormalMaterial.new
MeshBasicMaterial = THREE.MeshBasicMaterial.new
MeshPhongMaterial = THREE.MeshPhongMaterial.new
MeshStandardMaterial = THREE.MeshStandardMaterial.new
MeshDepthMaterial = THREE.MeshDepthMaterial.new
PointsMaterial = THREE.PointsMaterial.new
SpriteMaterial = THREE.SpriteMaterial.new
TextureLoader = THREE.TextureLoader.new

Mesh = THREE.Mesh.new
Points = THREE.Points.new
Line = THREE.Line.new
Sprite = THREE.Sprite.new

Scene = THREE.Scene.new
PerspectiveCamera = THREE.PerspectiveCamera.new
CameraHelper = THREE.CameraHelper.new
WebGLRenderer = THREE.WebGLRenderer.new
PCFSoftShadowMap = THREE.PCFSoftShadowMap

OrbitControls = THREE.OrbitControls.new
FlyControls = THREE.FlyControls.new
FirstPersonControls = THREE.FirstPersonControls.new

OBJLoader = THREE.OBJLoader.new
AmbientLight = THREE.AmbientLight.new
DirectionalLight = THREE.DirectionalLight.new
SpotLight = THREE.SpotLight.new
PointLight = THREE.PointLight.new
PointLightHelper = THREE.PointLightHelper.new
PCFSoftShadowMap = THREE.PCFSoftShadowMap

Matrix4 = THREE.Matrix4.new
Vector3 = THREE.Vector3.new
Vector2 = THREE.Vector2.new
Clock = THREE.Clock.new
